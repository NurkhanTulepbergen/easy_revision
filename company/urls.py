from django.urls import path
from .views import CompanyAPIView, ReportForCompanyAPIView, company_list, company_detail, report_list

urlpatterns = [
    path('companies/', company_list, name='company_list'),
    path('companies/<int:pk>/', company_detail, name='company_detail'),
    path('company/reports/', report_list, name='report_list'),
    path('companies/', CompanyAPIView.as_view(), name='company_list'),
    path('companies/<int:pk>/', CompanyAPIView.as_view(), name='company_detail'),
    path('company/reports/', ReportForCompanyAPIView.as_view(), name='report_list'),
    path('company/reports/<int:pk>/', ReportForCompanyAPIView.as_view(), name='report_detail'),
]
