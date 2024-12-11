from django.db import models
from company.models import Company
from notification.models import StoreNotification

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_product')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    barcode = models.CharField(max_length=255, null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    minimum_quantity = models.PositiveIntegerField(default=5)

    def save(self, *args, **kwargs):
        if self.quantity < self.minimum_quantity:
            self.send_low_stock_notification()
        super().save(*args, **kwargs)

    def send_low_stock_notification(self):
        store = self.company.user.store_user
        StoreNotification.objects.create(
            store=store,
            message=f"Product {self.name} is below the minimum stock level.",
        )
