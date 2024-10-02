from django.urls import path, include
from videos.views.admin import AdminVideoViews


urlpatterns = [
    path('videos/', AdminVideoViews.as_view(), name='front-video-list'),  # برای لیست ویدیوها و ایجاد ویدیو جدید (GET و POST)
    path('videos/<int:pk>/', AdminVideoViews.as_view(), name='front-video-detail'),  # برای جزئیات ویدیو، بروزرسانی و حذف ویدیو (GET، PUT و DELETE)
]
