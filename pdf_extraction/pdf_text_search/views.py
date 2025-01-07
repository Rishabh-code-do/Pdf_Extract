from django.shortcuts import redirect, render

import os
import re
from django.shortcuts import render
from django.http import JsonResponse
from .models import Reasoning
from .forms import PDFUploadForm
import pdfplumber
from datetime import datetime
from django.db import models


# Store reasoning in the database
def store_reasoning(reasoning,access_tag):
    Reasoning.objects.create(
        content=reasoning["content"],
        date=reasoning["date"],
        version_tag=reasoning["version_tag"],
        security_tag=reasoning["security_tag"],
        access_tag=access_tag,
    )


# Split text by versions
def split_versions(text):
    # Match sections like "Version 1:" or "Version 2:"
    version_chunks = re.split(r"(Version \d+:)", text)
    sections = []
    
    for i in range(1, len(version_chunks), 2):
        header = version_chunks[i]
        body = version_chunks[i + 1] if i + 1 < len(version_chunks) else ""
        sections.append((header, body.strip()))
    return sections

# Extract reasoning and metadata from a PDF section
def extract_metadata(chunk):
    patterns = {
        "content": r"Mathematical reasoning:\s*\"(.*?)\"(?=\s*Date:)",  # Capture text inside quotes
        "date": r"Date:\s*([\d-]+)",
        "version_tag": r"Version tag:\s*(v[\d.]+)",
        "security_tag": r"Security tag:\s*(\w+)",
    }
    # Extract matches
    matches = {key: re.search(pattern, chunk, re.DOTALL) for key, pattern in patterns.items()}

    # Validate and return metadata if all matches are found
    if all(matches.values()):
        return {
            "content": matches["content"].group(1).strip(),  # Extract text inside quotes
            "date": matches["date"].group(1),
            "version_tag": matches["version_tag"].group(1),
            "security_tag": matches["security_tag"].group(1),
        }
    return None

# Process a single PDF file
def process_pdf(file_path,access_tag):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text().replace("\n", " ")

    # Split by version and process each
    sections = split_versions(text)
    for header, chunk in sections:
        metadata = extract_metadata(chunk)
        store_reasoning(metadata,access_tag)

# Upload PDF view
def upload_pdf(request):
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data["pdf_file"]
            file_path = os.path.join("uploads", pdf_file.name)
            access_tag= form.cleaned_data["access_tag"]
            os.makedirs("uploads", exist_ok=True)
            with open(file_path, "wb+") as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)
            process_pdf(file_path,access_tag)
            return redirect('uploaded_pdf_page')
    else:
        form = PDFUploadForm()
    return render(request, "upload.html", {"form": form})

# Uploaded PDF options page
def uploaded_pdf_page(request):
    return render(request, "uploaded_pdf_page.html")


# Query reasoning view
def query_reasoning(request):
    date = request.GET.get("date")
    security_tag = request.GET.get("security_tag")
    access_tag = request.GET.get("access_tag")

    queryset = Reasoning.objects.all()
    if date:
        # Convert the date from string to a datetime object for comparison
        query_date = datetime.strptime(date, "%Y-%m-%d").date()

        print(query_date)
        
        # Find reasoning closest to the given date
        queryset = queryset.annotate(date_diff=models.Func(
            models.F('date') - models.Value(query_date),
            function='ABS',
            output_field=models.IntegerField(),
        ))

        # Order by the smallest date difference first
        queryset = queryset.order_by('date_diff', '-version_tag')  # In case of tie, order by version_tag

    if security_tag:
        queryset = queryset.filter(security_tag=security_tag)

    if access_tag:
        queryset = queryset.filter(access_tag=access_tag)

    # Fetch results
    results = [
        {
            "content": obj.content,
            "date": obj.date,
            "version_tag": obj.version_tag,
            "security_tag": obj.security_tag,
            "access_tag": obj.access_tag
        }
        for obj in queryset
    ]
    
    return JsonResponse({"result": results[0]})
