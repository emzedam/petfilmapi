# categories/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from categories.views.front import FrontCategoryViewSet

router = DefaultRouter()
router.register(r'categories', FrontCategoryViewSet, basename='front-category')

urlpatterns = [
    path('', include(router.urls)),
]