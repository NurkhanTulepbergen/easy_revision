from django.urls import path
from .views import login_page, user_register, logout_user


# Регистрация и логин
urlpatterns = [
    path('', login_page, name='login'),  # URL для страницы логина
    path('register/', user_register, name='register'),  # URL для страницы регистрации
    path('logout/', logout_user, name='logout'),
]

