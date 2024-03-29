# views.py
from .forms import UploadFileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Page, UploadedPDF
import fitz
import os
from django.contrib.auth import logout
import shutil
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .utils import analyze_invoice , hello
import json
import pandas as pd
from django.http import HttpResponse
from io import BytesIO

@login_required
def export_to_excel(request):
    if request.method == 'POST':
        result_dict = request.POST.get('result_dict')
        # Convert the result_dict string back to a dictionary
        result_dict = eval(result_dict)

        # Create a DataFrame from the result_dict
        df = pd.DataFrame(list(result_dict.items()), columns=['Keys', 'Values'])

        # Prepare Excel file in memory
        excel_file = BytesIO()
        with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)

        # Rewind the buffer
        excel_file.seek(0)

        # Set up response
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="result_pdf.xlsx"'
        response['Content-Transfer-Encoding'] = 'binary'
        return response
    else:
        return HttpResponse("Invalid request")

@login_required
def process_pdf(request):
    if request.method == 'POST':
        # Get the JSON string of checked page URLs from the form data
        urls = request.POST.get('checked_page_urls')
        checked_page_urls = urls.split(',')[0]
        # print(checked_page_urls)
        # Perform PDF analysis
        checked_page_urls="D:\DJANGO\Blue Consulting Ocr\BC_OCR"+ checked_page_urls
        
        result_dict = analyze_invoice(checked_page_urls)
        # result_dict = hello(checked_page_urls)
        rowspan_value = 1
        taxspan_value = 1
        for key, value in result_dict.items():
            
            if key == "Invoice items:":
                rowspan_value = len(value) + 1
            elif key == "Tax Items":
                taxspan_value = len(value) + 1
                
            
            
                

        # Render a template with the result_dict
        return render(request, 'result.html', {'result_dict': result_dict, 'rowspan_value': rowspan_value,
                                               'taxspan_value': taxspan_value})

def process_uploaded_pdf(request,uploaded_pdf):
    
    # Save the new uploaded PDF file
    uploaded_pdf.save()
    # Assuming user is the currently logged-in user
    user = request.user
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
                user=user,
                uploaded_pdf=uploaded_pdf,
                page=page_path,
                page_number=page_num + 1
            )
def delete_user_data(request):
    try:
        user = request.user
        # Get records from UploadedPDF table for the logged-in user
        user_uploaded_pdfs = UploadedPDF.objects.filter(user=user)
        # Get records from Page table for the logged-in user
        # print(user)
        user_pages = Page.objects.filter(user=user)
        # Delete files from pdf_page/ directory based on URLs stored in Page objects
        for page in user_pages:
            # print(page.id, page.page, page.page_number, page.uploaded_pdf_id, page.user_id)
            page_file_path = page.page.path
            if os.path.exists(page_file_path):
                os.remove(page_file_path)

        # Delete records from Page table for the logged-in user
        user_pages.delete()

        # Delete files from pdf_file/ directory based on URLs stored in UploadedPDF objects
        for uploaded_pdf in user_uploaded_pdfs:
            pdf_file_path = uploaded_pdf.pdf_file.path
            
            if os.path.exists(pdf_file_path):
                
                os.remove(pdf_file_path)
                

        # Delete records from UploadedPDF table for the logged-in user
        user_uploaded_pdfs.delete()


        
    except:
        pass

@login_required
def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Delete existing PDF and its associated pages, if any
            try:
                delete_user_data(request)

            except UploadedPDF.DoesNotExist:
                pass
            uploaded_pdf = form.save(commit=False)
            uploaded_pdf.user = request.user  # Assign the logged-in user
            uploaded_pdf.save()
             # Print the path to the uploaded file
            
            process_uploaded_pdf(request,uploaded_pdf)

            return redirect('display_pdf', pdf_id=uploaded_pdf.id)  # Redirect to display page with PDF ID
    else:
        form = UploadFileForm()
    return render(request, 'home.html', {'form': form})


@login_required
def display_pdf(request, pdf_id):
    uploaded_pdf = get_object_or_404(UploadedPDF, pk=pdf_id)
    pages = Page.objects.filter(uploaded_pdf_id=pdf_id)
    return render(request, 'display_pdf.html', {'uploaded_pdf': uploaded_pdf, 'pages': pages})

@login_required
def display_all_pdf(request):
    # Retrieve all PDF files from the Page model
    user = request.user
    pdf_files = Page.objects.filter(user=user)

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

def logout_view(request):
    logout(request)
    
    return redirect('/login')

def base_view(request):
    return render(request, 'base.html')