# Generated by Django 5.0.3 on 2024-12-06 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='image',
        ),
    ]