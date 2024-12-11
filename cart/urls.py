from django.urls import path
from .views import CartAPIView, CartItemsAPIView, cart_list, cart_checkout, add_to_cart, update_cart_item

urlpatterns = [
    # Отображение корзины и оформление заказа
    path('cart/', cart_list, name='cart_list'),
    path('cart/checkout/', cart_checkout, name='cart_checkout'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/item/<int:cart_item_id>/update/', update_cart_item, name='update_cart_item'),

    # API для работы с корзинами
    path('api/carts/', CartAPIView.as_view(), name='api_cart_list'),
    path('api/carts/<int:pk>/', CartAPIView.as_view(), name='api_cart_detail'),

    # API для работы с элементами корзины
    path('api/carts/<int:cart_pk>/items/', CartItemsAPIView.as_view(), name='api_cart_items_list'),
    path('api/carts/<int:cart_pk>/items/create/', CartItemsAPIView.as_view(), name='api_cart_items_create'),
    path('api/items/<int:pk>/', CartItemsAPIView.as_view(), name='api_cart_item_detail'),
    path('api/items/<int:pk>/update/', CartItemsAPIView.as_view(), name='api_cart_item_update'),
    path('api/items/<int:pk>/delete/', CartItemsAPIView.as_view(), name='api_cart_item_delete'),
]
