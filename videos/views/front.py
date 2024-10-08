from rest_framework import viewsets, filters
from videos.models import Video
from videos.serializers import VideoSerializer


class FrontVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_fa' , 'title_en']