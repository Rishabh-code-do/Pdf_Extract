from django.urls import path
from .views import upload_pdf, query_reasoning , uploaded_pdf_page

urlpatterns = [
    path("upload/", upload_pdf, name="upload_pdf"),
    path('uploaded_pdf_page/', uploaded_pdf_page, name='uploaded_pdf_page'),
    path("query/", query_reasoning, name="query_reasoning"),
]
