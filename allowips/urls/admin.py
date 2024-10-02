from django.urls import path, include
from rest_framework.routers import DefaultRouter
from allowips.views.admin import AllowedApiView

router = DefaultRouter()
router.register(r"ip" , AllowedApiView , basename="router-ips")

urlpatterns = [
    path('', include(router.urls))
]