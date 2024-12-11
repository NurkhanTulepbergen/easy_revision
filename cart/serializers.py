from rest_framework import serializers
from .models import Cart, CartItems

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'store', 'created_at', 'updated_at', 'is_active']


class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ['id', 'cart', 'product', 'quantity', 'get_cost']
