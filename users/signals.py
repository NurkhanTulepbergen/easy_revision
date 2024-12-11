from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from store.models import Store
from company.models import Company

@receiver(post_save, sender=User)
def create_store_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'store':  # Проверяем, что пользователь создан и его роль - Store
        Store.objects.create(user=instance, name=f"Store for {instance.username}")
    elif created and instance.role == 'company':
        Company.objects.create(user=instance, name=f"Store for {instance.username}")

@receiver(post_save, sender=User)
def save_store_profile(sender, instance, **kwargs):
    if instance.role == 'store' and hasattr(instance, 'store_profile'):
        instance.store_profile.save()
    elif instance.role == 'company' and hasattr(instance, 'company_user'):
        instance.company_user.save()


