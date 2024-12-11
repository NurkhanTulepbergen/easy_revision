# Import necessary modules and models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from requests import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import *
from .serializers import CustomUserCreateSerializer
from django.contrib.auth import logout



# Define a view function for the login page
def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/')

        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)

        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('/')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect('/api/')

    # Render the login page template (GET request)
    return render(request, 'login.html')


# Регистрация пользователя
def user_register(request):
    if request.method == 'POST':
        # Сохраняем данные пользователя с использованием сериализатора
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = User.objects.create_user(username=username, email=email, password=password, role=role)
        messages.success(request, 'Account created successfully')
        return redirect('login')  # Перенаправление на страницу логина после успешной регистрации

    return render(request, 'register.html')


# API для создания нового пользователя
class CustomUserViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Используем сериализатор для создания нового пользователя
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'User created successfully'}, status=201)
        return Response(serializer.errors, status=400)



def logout_user(request):
    # Завершаем сессию пользователя
    logout(request)
    # Перенаправляем на страницу логина или главную страницу
    return redirect('login')
