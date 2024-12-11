# store/models.py
from django.utils import timezone

from django.db import models
from django.db.models import Sum

from order.models import OrderItem
from users.models import User

class Store(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store_user')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=13)

class ReportForStore(models.Model):
    REPORT_CHOICES = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=10, choices=REPORT_CHOICES)
    date = models.DateField(default=timezone.now)  # Дата отчета

    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Доход
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Расходы
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Чистая прибыль

    def __str__(self):
        return f"{self.report_type.capitalize()} Report for {self.store.name} on {self.date}"

    def generate_report(self):
        """Метод для генерации отчета по типу (день, месяц, год)"""
        if self.report_type == 'daily':
            self.generate_daily_report()
        elif self.report_type == 'monthly':
            self.generate_monthly_report()
        elif self.report_type == 'yearly':
            self.generate_yearly_report()

    def generate_daily_report(self):
        """Генерация ежедневного отчета"""
        today = timezone.now().date()
        order_items = OrderItem.objects.filter(order__store=self.store, order__created_at__date=today)

        total_revenue = 0
        total_expenses = 0
        total_profit = 0

        for item in order_items:
            total_revenue += item.get_cost()
            total_expenses += item.get_expense()
            total_profit += item.get_profit()

        self.total_revenue = total_revenue
        self.total_expenses = total_expenses
        self.total_profit = total_profit
        self.save()

    def generate_monthly_report(self):
        """Генерация месячного отчета"""
        month_start = timezone.now().replace(day=1)
        month_end = timezone.now().replace(day=28) + timezone.timedelta(days=4)  # Конец месяца

        order_items = OrderItem.objects.filter(
            order__store=self.store,
            order__created_at__gte=month_start,
            order__created_at__lte=month_end
        )

        total_revenue = 0
        total_expenses = 0
        total_profit = 0

        for item in order_items:
            total_revenue += item.get_cost()
            total_expenses += item.get_expense()
            total_profit += item.get_profit()

        self.total_revenue = total_revenue
        self.total_expenses = total_expenses
        self.total_profit = total_profit
        self.save()

    def generate_yearly_report(self):
        """Генерация годового отчета"""
        year_start = timezone.now().replace(month=1, day=1)
        year_end = timezone.now().replace(month=12, day=31)

        order_items = OrderItem.objects.filter(
            order__store=self.store,
            order__created_at__gte=year_start,
            order__created_at__lte=year_end
        )

        total_revenue = 0
        total_expenses = 0
        total_profit = 0

        for item in order_items:
            total_revenue += item.get_cost()
            total_expenses += item.get_expense()
            total_profit += item.get_profit()

        self.total_revenue = total_revenue
        self.total_expenses = total_expenses
        self.total_profit = total_profit
        self.save()
