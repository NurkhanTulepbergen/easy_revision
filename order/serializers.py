from rest_framework import serializers
from .models import Order, OrderItem

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'store', 'company', 'status', 'created_at', 'updated_at', 'total_revenue', 'total_expenses', 'total_profit']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'get_cost', 'get_expense', 'get_profit']
