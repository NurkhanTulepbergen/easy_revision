from rest_framework import serializers
from .models import Store, ReportForStore

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'user', 'name', 'description', 'address', 'contact']


class ReportForStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportForStore
        fields = '__all__'
        read_only_fields = ['total_revenue', 'total_expenses', 'total_profit']  # Эти поля заполняются автоматически
