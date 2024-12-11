from rest_framework.permissions import BasePermission

class IsStore(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'store'

class IsCompany(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'company'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
