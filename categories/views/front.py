
from rest_framework import viewsets
from categories.models import Category
from categories.serializers import CategoryListSerializer
from rest_framework.response import Response
from videos.serializers import VideoSerializer
class FrontCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.get_root_nodes()  # دریافت تمام دسته‌ها
    serializer_class = CategoryListSerializer  # مشخص کردن سریالایزر
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # دریافت شیء دسته‌بندی
        serializer = self.get_serializer(instance)  # سریالایز کردن دسته‌بندی

        # دریافت ویدیوهای مرتبط با این دسته‌بندی
        videos = instance.videos.all()  # ویدیوهای مرتبط
        video_serializer = VideoSerializer(videos, many=True)

        # ساخت پاسخ
        return Response({
            'category': serializer.data,
            'related_videos': video_serializer.data  # ویدیوهای مرتبط
        })
    
    
    