from django.urls import path, include
from rest_framework.routers import DefaultRouter

from regularusers.views.admin import AdminRegularUserViews

router = DefaultRouter()
router.register(r"users" , AdminRegularUserViews , basename="admin-manage-users")

urlpatterns = [
    path('' , include(router.urls))
]