from django.urls import path, include
from videos.views.front import FrontVideoViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'videos', FrontVideoViewSet, basename='front-videos')

urlpatterns = [
    path('', include(router.urls)),
]
