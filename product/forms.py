from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['company', 'category', 'name', 'description', 'sale_price', 'barcode', 'purchase_price', 'quantity', 'minimum_quantity']

    def clean_purchase_price(self):
        purchase_price = self.cleaned_data.get('purchase_price')
        if purchase_price is None or purchase_price <= 0:
            raise forms.ValidationError("Цена покупки должна быть положительным числом.")
        return purchase_price
