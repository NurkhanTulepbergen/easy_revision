# order/models.py
from django.db import models
from django.db.models import Sum

from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    store = models.ForeignKey('store.Store', on_delete=models.CASCADE)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.store.username}"

    def calculate_profit_and_loss(self):
        revenue = 0
        expenses = 0
        profit = 0
        for item in self.items.all():
            revenue += item.get_cost()
            expenses += item.get_expense()
            profit += item.get_profit()

        self.total_revenue = revenue
        self.total_expenses = expenses
        self.total_profit = profit
        self.save()

    def update_product_quantity(self):
        if self.status == 'completed':
            for item in self.items.all():
                item.product.quantity -= item.quantity
                item.product.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order #{self.order.id}"

    def get_cost(self):
        return self.quantity * self.product.sale_price

    def get_expense(self):
        return self.quantity * self.product.purchase_price

    def get_profit(self):
        return (self.product.sale_price - self.product.purchase_price) * self.quantity
