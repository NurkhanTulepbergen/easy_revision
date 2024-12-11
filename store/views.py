from rest_framework.decorators import permission_classes

from users.permissions import IsStore
from .serializers import StoreSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReportForStoreSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .forms import StoreUpdateForm
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import ReportForStore
from .forms import ReportForStoreForm

@permission_classes([IsStore])
def create_report(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    try:
        # Получаем текущий магазин пользователя
        current_store = request.user.store_user
    except AttributeError:
        return render(request, 'error.html', {"message": "User does not have an associated store."})

    if request.method == 'POST':
        form = ReportForStoreForm(request.POST)
        if form.is_valid():
            # Создаём отчёт, связанный с текущим магазином
            report = form.save(commit=False)
            report.store = current_store
            report.save()
            report.generate_report()  # Генерация данных отчёта
            return redirect('store_reports')  # Перенаправляем на страницу с отчётами
    else:
        form = ReportForStoreForm()

    return render(request, 'create_report.html', {'form': form})


@permission_classes([IsStore])
def current_store_detail(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to view this page.")

    try:
        # Получаем магазин, связанный с текущим пользователем
        current_store = request.user.store_user
    except AttributeError:
        return render(request, 'error.html', {"message": "User does not have an associated store."})

    message = None
    if request.method == 'POST':
        form = StoreUpdateForm(request.POST, instance=current_store)
        if form.is_valid():
            form.save()
            message = "Данные успешно обновлены!"
            # Создаём новую пустую форму, не связанную с объектом
            form = StoreUpdateForm()
        else:
            message = "Произошла ошибка. Проверьте данные."
    else:
        # Изначально передаем форму с текущими данными магазина
        form = StoreUpdateForm()

    return render(request, 'store_detail.html', {'store': current_store, 'form': form, 'message': message})




@permission_classes([IsStore])
def current_store_reports(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to view this page.")

    try:
        # Получаем магазин текущего пользователя
        current_store = request.user.store_user
    except AttributeError:
        return render(request, 'error.html', {"message": "User does not have an associated store."})

    # Получаем все отчеты, связанные с этим магазином
    reports = ReportForStore.objects.filter(store=current_store)

    # Передаем отчеты в шаблон
    return render(request, 'store_reports.html', {'reports': reports, 'store': current_store})

class StoreAPIView(APIView):
    permission_classes = [IsStore]  # Только для авторизованных пользователей

    def get(self, request):
        try:
            # Получаем магазин, связанный с текущим пользователем
            current_store = request.user.store_user
        except AttributeError:
            return Response({"message": "User does not have an associated store."}, status=status.HTTP_403_FORBIDDEN)

        # Сериализуем информацию о текущем магазине
        serializer = StoreSerializer(current_store)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        try:
            # Получаем магазин текущего пользователя
            current_store = request.user.store_user
        except AttributeError:
            return Response({"message": "User does not have an associated store."}, status=status.HTTP_403_FORBIDDEN)

        # Обновляем данные магазина
        serializer = StoreSerializer(current_store, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            # Получаем магазин текущего пользователя
            current_store = request.user.store_user
        except AttributeError:
            return Response({"message": "User does not have an associated store."}, status=status.HTTP_403_FORBIDDEN)

        # Удаляем магазин
        current_store.delete()
        return Response({"message": "Store deleted successfully."}, status=status.HTTP_204_NO_CONTENT)





class ReportForStoreAPIView(APIView):
    permission_classes = [IsStore]  # Только для авторизованных пользователей

    def get(self, request, pk=None):
        # Получаем текущий магазин, связанный с пользователем
        try:
            current_store = request.user.store_user
        except AttributeError:
            return Response({"message": "User does not have an associated store."}, status=status.HTTP_403_FORBIDDEN)

        if pk:  # Если передан ID отчета
            report = get_object_or_404(ReportForStore, pk=pk, store=current_store)
            serializer = ReportForStoreSerializer(report)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:  # Если ID не передан, возвращаем все отчеты для текущего магазина
            reports = ReportForStore.objects.filter(store=current_store)
            serializer = ReportForStoreSerializer(reports, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Ограничиваем создание отчета только для текущего магазина
        try:
            current_store = request.user.store_user
        except AttributeError:
            return Response({"message": "User does not have an associated store."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['store'] = current_store.id  # Устанавливаем текущий магазин

        serializer = ReportForStoreSerializer(data=data)
        if serializer.is_valid():
            report = serializer.save()
            report.generate_report()  # Генерация данных для отчета
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

