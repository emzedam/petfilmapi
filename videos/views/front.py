from rest_framework import viewsets
from videos.models import Video
from videos.serializers import VideoSerializer


class FrontVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer