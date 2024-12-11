from django.db.models.signals import post_save
from django.dispatch import receiver
from notification.models import Notification
from .models import Order

@receiver(post_save, sender=Order)
def order_status_updated(sender, instance, created, **kwargs):
    """Сигнал для обновления количества продуктов при изменении статуса заказа на completed"""
    if instance.status == 'completed':
        instance.update_product_quantity()  # Обновление количества товаров в магазине


@receiver(post_save, sender=Order)
def send_notification_to_company(sender, instance, created, **kwargs):
    """Сигнал для отправки уведомления компании при создании нового заказа"""
    if created:
        # Создаем уведомление для компании
        Notification.objects.create(
            company=instance.company,  # Компания, связанная с заказом
            order=instance,  # Заказ
            message=f"You have received a new order from store {instance.store.name}.",  # Сообщение уведомления
        )
