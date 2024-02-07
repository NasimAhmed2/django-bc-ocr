from django.db import models

# Create your models here.
# myapp/models.py
from django.db import models

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Add any additional user-related fields as needed

# myapp/views.py
from django.shortcuts import render

class UploadedPDF(models.Model):
    pdf_file = models.FileField(upload_to='pdf_files/')
    upload_time = models.DateTimeField(auto_now_add=True)

 # Add this field to store the page number

class Page(models.Model):
    uploaded_pdf = models.ForeignKey(UploadedPDF, related_name='pages', on_delete=models.CASCADE)
    page = models.FileField(upload_to='pdf_pages/')
    page_number = models.IntegerField()