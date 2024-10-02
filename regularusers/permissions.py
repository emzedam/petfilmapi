from rest_framework.permissions import BasePermission

class IsAuthenticated(BasePermission):
    """
    اجازه می‌دهد تا کاربران غیر احراز هویت‌شده به برخی عملیات‌ها دسترسی داشته باشند.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated