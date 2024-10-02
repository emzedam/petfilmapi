
from django.http import JsonResponse
from .models import AlloweIps
from rest_framework import status

class IPFilterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # بررسی اینکه آیا درخواست به پنل ادمین است
        if request.path.startswith('/admin/'):
            return self.get_response(request)
        
        ip = request.META.get('REMOTE_ADDR')
        # print(ip)
        if not AlloweIps.objects.filter(ip_address=ip , is_active=True).exists():
            return JsonResponse({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        response = self.get_response(request)
        return response
