# Pdf_Extract/forms.py

from django import forms
from .models import UploadedPDF

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedPDF
        fields = ['pdf_file']
