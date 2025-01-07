from django import forms

class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField()
    access_tag = forms.CharField(max_length=20,required=False)
