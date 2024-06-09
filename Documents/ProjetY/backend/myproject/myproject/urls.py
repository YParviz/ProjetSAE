# urls.py
from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import LogoutView, create_company, get_companies, get_company, delete_company,upload_document, get_document_status
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.ignore_login),  # Ignorer la route /login/
    path('admin/', admin.site.urls),
    path('api/users/', views.get_users, name='api_get_users'),
    path('api/validate/<int:user_id>/', views.validate_user, name='validate_user'),
    path('api/user-details/<int:user_id>/', views.get_user_details, name='get_user_details'),
    path('api/register/', views.register_user, name='register_user'),
    path('api/login/', views.login_user, name='login_user'),
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/user/', views.get_user, name='api_get_user'),
    path('api/create-company/', create_company, name='create-company'),  # Correction ici
    path('api/companies/', get_companies, name='get-companies'),  # Nouvelle route pour récupérer les entreprises
        path('api/companies/<int:company_id>/', get_company, name='get-company'),  # Nouvelle route pour obtenir une entreprise spécifique
    path('api/companies/<int:company_id>/delete/', delete_company, name='delete-company'),  # Nouvelle route pour supprimer une entreprise
     path('api/companies/upload-document/', upload_document, name='upload-document'),
    path('api/companies/<int:company_id>/document-status/', get_document_status, name='get-document-status'),
        path('api/logout/', LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
