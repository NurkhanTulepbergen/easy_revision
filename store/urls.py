from django.urls import path
from .views import StoreAPIView, ReportForStoreAPIView, current_store_detail, current_store_reports, create_report

urlpatterns = [
    path('store/', StoreAPIView.as_view(), name='current_store'),
    path('store/detail/', current_store_detail, name='store_detail'),
    path('reports/create/', create_report, name='create_report'),
    path('reports/', current_store_reports, name='store_reports'),
    path('store/reports/', ReportForStoreAPIView.as_view(), name='reports_list'),
    path('store/reports/<int:pk>/', ReportForStoreAPIView.as_view(), name='report_detail'),
]
