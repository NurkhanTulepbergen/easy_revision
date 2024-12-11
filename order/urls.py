from django.urls import path
from .views import OrderAPIView, OrderItemAPIView, order_history, order_detail_view

urlpatterns = [
    path('orders/', order_history, name='order_history'),
    path('orders/<int:pk>/', order_detail_view, name='order_detail'),
    path('orders/', OrderAPIView.as_view(), name='order_list'),  # GET (all orders) or POST (create order)
    path('orders/<int:pk>/', OrderAPIView.as_view(), name='order_detail'),  # GET (order by pk), PUT (update), DELETE (delete)
    path('orders/<int:order_pk>/items/', OrderItemAPIView.as_view(), name='order_items_list'),# List all items in a specific order or create a new one
    path('orders/<int:order_pk>/items/<int:pk>/', OrderItemAPIView.as_view(), name='order_item_detail'),# Get, update, or delete a specific order item
]
