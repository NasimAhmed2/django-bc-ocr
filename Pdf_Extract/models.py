from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# myapp/models.py
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)



class UploadedPDF(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    pdf_file = models.FileField(upload_to='pdf_files/')
    upload_time = models.DateTimeField(auto_now_add=True)

 # Add this field to store the page number

class Page(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    uploaded_pdf = models.ForeignKey(UploadedPDF, related_name='pages', on_delete=models.CASCADE)
    page = models.FileField(upload_to='pdf_pages/')
    page_number = models.IntegerField()