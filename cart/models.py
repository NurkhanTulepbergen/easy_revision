from django.db import models

class Cart(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart for {self.store.name} created at {self.created_at}"

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.cart_items.all())
        return total_cost

    def checkout(self):
        """
        Переводит товары из корзины в историю заказов и очищает корзину.
        """
        from order.models import Order, OrderItem  # Импортируем модель заказа

        if not self.cart_items.exists():
            return None  # Нельзя оформить заказ с пустой корзиной

        # Создаем новый заказ
        order = Order.objects.create(
            store=self.store,
            company=self.cart_items.first().product.company,  # Предполагается, что продукт связан с компанией
            total_revenue=self.get_total_cost(),
            status='pending'
        )

        # Переносим элементы корзины в заказ
        for cart_item in self.cart_items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
            cart_item.product.quantity -= cart_item.quantity
            cart_item.product.save()

        # Очищаем корзину
        self.cart_items.all().delete()
        return order

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart"

    def get_cost(self):
        return self.product.sale_price * self.quantity
