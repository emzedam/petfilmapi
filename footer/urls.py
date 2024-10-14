from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FooterDescriptionViewSet, FooterLinkViewSet

router = DefaultRouter()
router.register(r'footer-description', FooterDescriptionViewSet)
router.register(r'footer-links', FooterLinkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
