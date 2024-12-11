from rest_framework.decorators import permission_classes

from product.models import Product
from store.models import Store
from users.permissions import IsStore
from .models import Cart, CartItems
from .serializers import CartSerializer, CartItemsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Cart, CartItems
import logging


api_logger = logging.getLogger('api_access')


@login_required
@permission_classes([IsStore])
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItems, id=cart_item_id)

    # Получаем количество из формы
    new_quantity = request.POST.get(f'quantity_{cart_item.id}')

    if new_quantity and new_quantity.isdigit():
        cart_item.quantity = int(new_quantity)
        cart_item.save()

    return redirect('cart_list')  # Перенаправляем на страницу корзины


@login_required
@permission_classes([IsStore])
def add_to_cart(request, product_id):
    # Получаем продукт по ID
    product = get_object_or_404(Product, id=product_id)

    # Получаем или создаем активную корзину для пользователя
    store = request.user.store_user
    cart, created = Cart.objects.get_or_create(store=store, is_active=True)

    # Добавляем товар в корзину
    CartItems.objects.create(cart=cart, product=product, quantity=1)

    return redirect('cart_list')  # Перенаправляем на страницу корзины
@login_required
@permission_classes([IsStore])
def cart_list(request):
    # Получаем корзину, связанную с текущим магазином
    store = request.user.store_user
    cart = Cart.objects.filter(store=store, is_active=True).first()

    if not cart or not cart.cart_items.exists():
        return render(request, 'cart_list.html', {'cart': None, 'error': 'Ваша корзина пуста.'})

    return render(request, 'cart_list.html', {'cart': cart})

@login_required
@permission_classes([IsStore])
def cart_checkout(request):
    store = request.user.store_user
    # Получаем активную корзину
    cart = Cart.objects.filter(store=store, is_active=True).first()
    # Оформляем заказ
    order = cart.checkout()

    return redirect('order_history')





class CartAPIView(APIView):
    permission_classes = [IsStore]

    def get(self, request, pk=None):
        api_logger.debug(f"API accessed: {request.path}")
        if pk:
            try:
                cart = Cart.objects.get(pk=pk)
                serializer = CartSerializer(cart)
                return Response(serializer.data)
            except Cart.DoesNotExist:
                return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            carts = Cart.objects.all()
            serializer = CartSerializer(carts, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            cart = Cart.objects.get(pk=pk)
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)




class CartItemsAPIView(APIView):
    permission_classes = [IsStore]

    # Получить все элементы корзины
    def get(self, request, cart_pk=None, pk=None):
        if pk:  # Получить один элемент по его ID
            try:
                cart_item = CartItems.objects.get(pk=pk)
                serializer = CartItemsSerializer(cart_item)
                return Response(serializer.data)
            except CartItems.DoesNotExist:
                return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        elif cart_pk:  # Получить все элементы корзины по cart_pk
            cart_items = CartItems.objects.filter(cart_id=cart_pk)
            serializer = CartItemsSerializer(cart_items, many=True)
            return Response(serializer.data)
        else:  # Получить все элементы всех корзин
            cart_items = CartItems.objects.all()
            serializer = CartItemsSerializer(cart_items, many=True)
            return Response(serializer.data)

    # Создать новый элемент в корзине
    def post(self, request, cart_pk=None):
        serializer = CartItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart_id=cart_pk)  # Связываем с корзиной через cart_pk
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Обновить элемент корзины
    def put(self, request, cart_pk=None, pk=None):
        try:
            cart_item = CartItems.objects.get(pk=pk)
        except CartItems.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemsSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Удалить элемент из корзины
    def delete(self, request, cart_pk=None, pk=None):
        try:
            cart_item = CartItems.objects.get(pk=pk)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItems.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
