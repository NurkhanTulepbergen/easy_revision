from rest_framework.decorators import permission_classes

from users.permissions import IsCompany, IsStore
from .models import Company, ReportForCompany
from .serializers import CompanySerializer, ReportForCompanySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render

@permission_classes([IsStore])
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'company_list.html', {'companies': companies})

def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, 'company_detail.html', {'company': company})

def report_list(request):
    reports = ReportForCompany.objects.all()
    return render(request, 'report_list.html', {'reports': reports})




class CompanyAPIView(APIView):
    permission_classes = [IsCompany]  # Применяем ограничение

    def get(self, request, pk=None):
        if pk:
            company = Company.objects.get(pk=pk)
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        else:
            companies = Company.objects.all()
            serializer = CompanySerializer(companies, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        company = Company.objects.get(pk=pk)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = Company.objects.get(pk=pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReportForCompanyAPIView(APIView):
    permission_classes = [IsCompany]  # Применяем ограничение

    def get(self, request, pk=None):
        if pk:
            report = get_object_or_404(ReportForCompany, pk=pk)
            serializer = ReportForCompanySerializer(report)
            return Response(serializer.data)
        else:
            reports = ReportForCompany.objects.all()
            serializer = ReportForCompanySerializer(reports, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ReportForCompanySerializer(data=request.data)
        if serializer.is_valid():
            report = serializer.save()
            report.generate_report()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        report = get_object_or_404(ReportForCompany, pk=pk)
        serializer = ReportForCompanySerializer(report, data=request.data)
        if serializer.is_valid():
            report = serializer.save()
            report.generate_report()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        report = get_object_or_404(ReportForCompany, pk=pk)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
