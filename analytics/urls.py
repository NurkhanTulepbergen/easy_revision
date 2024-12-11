from django.shortcuts import render
from django.urls import path
from .views import product_trends

urlpatterns = [
    path('analytics/', product_trends, name='product_trends'),  # API endpoint
    path('analytics-view/', lambda request: render(request, 'analytics.html'), name='analytics_view'),  # Template view
]
