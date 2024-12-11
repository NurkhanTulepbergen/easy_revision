from rest_framework.decorators import permission_classes

from users.permissions import IsStore
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from .models import Order
from django.contrib.auth.decorators import login_required

@permission_classes([IsStore])
def order_detail_view(request, pk):
    # Получаем заказ по его ID или возвращаем 404
    order = get_object_or_404(Order, pk=pk)

    # Вычисляем общую стоимость всех товаров в заказе
    total_price = sum(item.get_cost() for item in order.items.all())

    return render(request, 'order_detail.html', {
        'order': order,
        'total_price': total_price,
    })
@login_required
@permission_classes([IsStore])
def order_history(request):
    # Получаем магазин текущего пользователя
    try:
        store = request.user.store_user
    except AttributeError:
        return render(request, 'order_history.html', {'orders': [], 'error': 'Store not found for this user.'})

    # Фильтруем заказы, связанные с этим магазином
    orders = Order.objects.filter(store=store)

    return render(request, 'order_history.html', {'orders': orders})
class OrderAPIView(APIView):
    permission_classes = [IsStore]

    # GET method to retrieve orders (either by store or a specific order by pk)
    def get(self, request, pk=None):
        if pk:
            # Retrieve specific order by pk
            try:
                order = Order.objects.get(pk=pk)
                serializer = OrderSerializer(order)
                return Response(serializer.data)
            except Order.DoesNotExist:
                return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Retrieve all orders
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)

    # POST method to create a new order
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT method to update an existing order
    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to delete an order by pk
    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class OrderItemAPIView(APIView):
    permission_classes = [IsStore]
    # Получить все элементы заказа
    def get(self, request, order_pk=None, pk=None):
        if pk:  # Получить один элемент по его ID
            try:
                order_item = OrderItem.objects.get(pk=pk)
                serializer = OrderItemSerializer(order_item)
                return Response(serializer.data)
            except OrderItem.DoesNotExist:
                return Response({"detail": "Order item not found."}, status=status.HTTP_404_NOT_FOUND)
        elif order_pk:  # Получить все элементы заказа по order_pk
            order_items = OrderItem.objects.filter(order_id=order_pk)
            serializer = OrderItemSerializer(order_items, many=True)
            return Response(serializer.data)
        else:  # Получить все элементы всех заказов
            order_items = OrderItem.objects.all()
            serializer = OrderItemSerializer(order_items, many=True)
            return Response(serializer.data)

    # Создать новый элемент в заказе
    def post(self, request, order_pk=None):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order_id=order_pk)  # Связываем с заказом через order_pk
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Обновить элемент заказа
    def put(self, request, order_pk=None, pk=None):
        try:
            order_item = OrderItem.objects.get(pk=pk)
        except OrderItem.DoesNotExist:
            return Response({"detail": "Order item not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderItemSerializer(order_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Удалить элемент из заказа
    def delete(self, request, order_pk=None, pk=None):
        try:
            order_item = OrderItem.objects.get(pk=pk)
            order_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except OrderItem.DoesNotExist:
            return Response({"detail": "Order item not found."}, status=status.HTTP_404_NOT_FOUND)
