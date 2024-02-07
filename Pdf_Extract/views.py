# views.py
from .forms import UploadFileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Page, UploadedPDF
import fitz
import os
import shutil
from django.contrib.auth.decorators import login_required

# def process_uploaded_pdf(uploaded_pdf):
#     # Open the uploaded PDF file
#     with uploaded_pdf.pdf_file.open('rb') as file:
#         # Open the PDF file using fitz
#         pdf_document = fitz.open(file)

#         # Iterate through each page of the PDF file
#         for page_num in range(len(pdf_document)):
#             # Get the page
#             page = pdf_document.load_page(page_num)
#             directory = 'pdf_pages/'
#             if not os.path.exists(directory):
#                 os.makedirs(directory)
#             page_path = f'pdf_pages/{uploaded_pdf.id}_page_{page_num + 1}.pdf'
#             new_doc = fitz.open()
#             new_doc.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
#             new_doc.save(page_path)
#             Page.objects.create(
#                 uploaded_pdf=uploaded_pdf,
#                 page=page_path,
#                 page_number=page_num + 1
#             )

def process_uploaded_pdf(uploaded_pdf):
    
    # Save the new uploaded PDF file
    uploaded_pdf.save()

    # Open the uploaded PDF file
    with uploaded_pdf.pdf_file.open('rb') as file:
        # Open the PDF file using fitz
        pdf_document = fitz.open(file)

        # Iterate through each page of the PDF file
        for page_num in range(len(pdf_document)):
            # Get the page
            page = pdf_document.load_page(page_num)
            directory = 'pdf_pages/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            page_path = f'pdf_pages/{uploaded_pdf.id}_page_{page_num + 1}.pdf'
            new_doc = fitz.open()
            new_doc.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
            new_doc.save(page_path)
            Page.objects.create(
                uploaded_pdf=uploaded_pdf,
                page=page_path,
                page_number=page_num + 1
            )
@login_required
def home(request):
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Delete existing PDF and its associated pages, if any
            try:
                # Delete all records from the database tables
                UploadedPDF.objects.all().delete()
                Page.objects.all().delete()
                # Delete the PDF file from the file system
                # Specify the directory path
                pdf_directory = 'pdf_pages/'
                pdf_directory1 = 'pdf_files/'
                # Use shutil.rmtree to remove the entire directory and its contents
                shutil.rmtree(pdf_directory)
                shutil.rmtree(pdf_directory1)
                # Create the directory again if needed
                os.makedirs(pdf_directory)
                os.makedirs(pdf_directory1)

            except UploadedPDF.DoesNotExist:
                pass
            uploaded_pdf = form.save()  # Save the uploaded PDF file to the database
            # Process the uploaded PDF file and save its pages to the database
             # Print the path to the uploaded file
            print("Path to uploaded PDF file:", uploaded_pdf.pdf_file.path)
            process_uploaded_pdf(uploaded_pdf)

            return redirect('display_pdf', pdf_id=uploaded_pdf.id)  # Redirect to display page with PDF ID
    else:
        form = UploadFileForm()
    return render(request, 'home.html', {'form': form})


@login_required
def display_pdf(request, pdf_id):
    uploaded_pdf = get_object_or_404(UploadedPDF, pk=pdf_id)
    pages = Page.objects.filter(uploaded_pdf_id=pdf_id)
    return render(request, 'display_pdf.html', {'uploaded_pdf': uploaded_pdf, 'pages': pages})

def display_all_pdf(request):
    # Retrieve all PDF files from the Page model
    pdf_files = Page.objects.all()

    return render(request, 'display_pdf1.html', {'pdf_files': pdf_files})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})