from rest_framework import viewsets, filters
from videos.models import Video
from videos.serializers import VideoSerializer


class FrontVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_fa' , 'title_en']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()

        # بررسی اینکه آیا شناسه ویدیو در URL موجود است
        video_id = self.kwargs.get('pk')  # یا استفاده از 'slug' در صورت استفاده از URL slug
        if video_id:
            try:
                # گرفتن ویدیو فعلی
                current_video = self.get_object()

                # گرفتن 10 ویدیو از همان دسته بندی
                related_videos = Video.objects.filter(
                    category=current_video.category
                ).exclude(id=current_video.id)[:10]

                # اضافه کردن ویدیوهای مشابه به context
                context['related_videos'] = related_videos
            except Video.DoesNotExist:
                context['related_videos'] = []  # اگر ویدیو وجود نداشت، یک لیست خالی
        else:
            context['related_videos'] = []  # اگر ID وجود نداشت، یک لیست خالی

        return context
