from rest_framework import serializers
from .models import Company, ReportForCompany

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['user', 'name', 'description', 'address', 'contact']


class ReportForCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportForCompany
        fields = ['company', 'report_type', 'date', 'total_revenue']
