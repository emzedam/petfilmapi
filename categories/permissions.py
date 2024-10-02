from rest_framework.permissions import BasePermission

class IsAuthenticated(BasePermission):
    """
    اجازه می‌دهد تا کاربران غیر احراز هویت‌شده به برخی عملیات‌ها دسترسی داشته باشند.
    """
    
    def has_permission(self, request, view):
        # اجازه دسترسی به GET (لیست) به همه کاربران
        # if request.method in ['GET']:
        #     return True
        
        # فقط کاربران احراز هویت‌شده می‌توانند سایر درخواست‌ها را انجام دهند
        return request.user.is_authenticated