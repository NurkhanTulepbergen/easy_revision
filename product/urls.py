from django.urls import path
from .views import product_list, update_product, delete_product, create_category, delete_category, home, add_product, edit_product

urlpatterns = [
    path('', home, name='home'),
    path('products/', product_list, name='product_list'),
    path('products/add/', add_product, name='add_product'),
    path('products/edit/<int:product_id>/', edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('products/update/<int:product_id>/', update_product, name='update_product'),
    path('category/create/', create_category, name='create_category'),
    path('category/delete/<int:category_id>/', delete_category, name='delete_category'),
]
