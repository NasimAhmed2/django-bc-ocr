# myapp/urls.py
from django.urls import path
from .views import home , display_pdf , display_all_pdf ,user_login ,signup
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', user_login, name='login'),
    path('signup', signup, name='signup'),
    path('home', home, name='home'),
    path('display_pdf/<int:pdf_id>/', display_pdf, name='display_pdf'),
    path('display_pdf/', display_all_pdf, name='display_all_pdf'),
    # Add other URLs as needed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
