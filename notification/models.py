from django.db import models

from order.models import Order
from store.models import Store


# Create your models here.
class Notification(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='company_notifications')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_notifications')  # Ссылка на заказ
    message = models.TextField(default="You have received a new order from store {store_name}")  # Сообщение уведомления
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания уведомления
    is_read = models.BooleanField(default=False)  # Статус прочтения уведомления

    def save(self, *args, **kwargs):
        # Заменяем {store_name} на имя магазина
        if not self.pk:  # Только если уведомление новое (не сохраненное еще)
            self.message = self.message.format(store_name=self.order.store.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Notification for {self.company.name} - Order #{self.order.id}"


class StoreNotification(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Статус прочтения уведомления

    def __str__(self):
        return f"Notification for {self.store.name} - {self.message}"

    def mark_as_read(self):
        """Метод для пометки уведомления как прочитанного"""
        self.is_read = True
        self.save()
