import os
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import UserProfile, Validation
from .serializers import CompanySerializer, UserProfileSerializer, ValidationSerializer
from rest_framework import status
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
from . import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.http import HttpResponseNotFound
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from .models import Company
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import logout


def ignore_login(request):
    return HttpResponse(status=204)

from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([AllowAny])
def get_users(request):
    try:
        print("Received request for user list")
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        print(f"Returning {len(users)} users")
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def get_user_details(request, user_id):
    user = UserProfile.objects.filter(user_id=user_id).first()
    if user:
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    else:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET', 'PATCH', 'DELETE'])
def validate_user(request, user_id):
    if request.method == 'GET':
        validation = get_object_or_404(Validation, user_profile__user_id=user_id)
        serializer = ValidationSerializer(validation)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        validation = get_object_or_404(Validation, user_profile__user_id=user_id)
        is_validated = request.data.get('is_validated', False)
        validation.is_validated = is_validated
        validation.save()
        return Response({'message': 'Validation status updated successfully'})
    
    elif request.method == 'DELETE':
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        if request.path.endswith('/icon.ico'):
            return HttpResponseNotFound()

        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        company = request.data.get('company')

        if not all([username, email, password, company]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        user_profile = UserProfile.objects.create(user=user, company=company)

        # Create the validation object for the user profile
        Validation.objects.create(user_profile=user_profile, is_validated=False)

        serializer = UserProfileSerializer(instance=user_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        user_profile = UserProfile.objects.get(user=user)
        if not user_profile.validation.is_validated:
            return Response({'error': 'User not validated'}, status=status.HTTP_400_BAD_REQUEST)
        
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'isAdmin': user.is_superuser,
            'username': user.username
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    try:
        # Récupérer l'utilisateur connecté à partir de la requête
        user = request.user
        
        # Récupérer les informations de l'utilisateur
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            # Ajoutez d'autres champs d'informations de l'utilisateur si nécessaire
            'isAdmin': user.is_superuser
        }
        # Retourner les informations de l'utilisateur
        return Response(user_data)
    except Exception as e:
        # En cas d'erreur, renvoyer une réponse avec un message d'erreur
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_company(request):
    company_name = request.data.get('company')
    if not company_name:
        return Response({'error': 'Company name is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        company = Company.objects.create(name=company_name)
        return Response({'message': 'Company created successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_companies(request):
    try:
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_company(request, company_id):
    try:
        company = get_object_or_404(Company, id=company_id)
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_company(request, company_id):
    try:
        company = get_object_or_404(Company, id=company_id)
        company.delete()
        return Response({'message': 'Company deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([AllowAny])
def upload_document(request):
    try:
        company_id = request.data.get('company_id')
        company = get_object_or_404(Company, id=company_id)

        document = request.FILES['document']

        # Définir le chemin de stockage
        upload_dir = os.path.join('media', 'documents', str(company_id))
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        document_path = os.path.join(upload_dir, document.name)

        with open(document_path, 'wb+') as destination:
            for chunk in document.chunks():
                destination.write(chunk)

        # Mettez à jour le statut de l'entreprise après le téléchargement du document
        company.status = 'Document Uploaded'
        company.save()

        return Response({'message': 'Document uploaded successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_document_status(request, company_id):
    try:
        company = get_object_or_404(Company, id=company_id)
        return Response({'status': company.status}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)