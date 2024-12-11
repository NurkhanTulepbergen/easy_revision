# company/models.py
from django.db import models

from order.models import OrderItem
from users.models import User
from django.utils import timezone

from django.db import models
from django.utils import timezone

class Company(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='company_user')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=13)

    def __str__(self):
        return self.name



class ReportForCompany(models.Model):
    REPORT_CHOICES = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=10, choices=REPORT_CHOICES)
    date = models.DateField(default=timezone.now)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.report_type.capitalize()} Report for {self.company.name} on {self.date}"

    def generate_report(self):
        if self.report_type == 'daily':
            self.generate_daily_report()
        elif self.report_type == 'monthly':
            self.generate_monthly_report()
        elif self.report_type == 'yearly':
            self.generate_yearly_report()

    def generate_daily_report(self):
        today = timezone.now().date()
        order_items = OrderItem.objects.filter(order__company=self.company, order__created_at__date=today)

        total_revenue = 0
        for item in order_items:
            total_revenue += item.get_cost()

        self.total_revenue = total_revenue
        self.save()

    def generate_monthly_report(self):
        month_start = timezone.now().replace(day=1)
        month_end = timezone.now().replace(day=28) + timezone.timedelta(days=4)

        order_items = OrderItem.objects.filter(
            order__company=self.company,
            order__created_at__gte=month_start,
            order__created_at__lte=month_end
        )

        total_revenue = 0
        for item in order_items:
            total_revenue += item.get_cost()

        self.total_revenue = total_revenue
        self.save()

    def generate_yearly_report(self):
        year_start = timezone.now().replace(month=1, day=1)
        year_end = timezone.now().replace(month=12, day=31)

        order_items = OrderItem.objects.filter(
            order__company=self.company,
            order__created_at__gte=year_start,
            order__created_at__lte=year_end
        )

        total_revenue = 0
        for item in order_items:
            total_revenue += item.get_cost()

        self.total_revenue = total_revenue
        self.save()
