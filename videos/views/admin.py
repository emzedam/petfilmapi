from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from videos.models import Video
from videos.serializers import VideoSerializer
from videos.permissions import IsAuthenticated
import os
import ffmpeg

class AdminVideoViews(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoSerializer
    
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            self.convert_to_hls(video)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(video, data=request.data)
        if serializer.is_valid():
            # حذف فایل‌های قبلی
            self.delete_video_files(video)
            video = serializer.save()
            self.convert_to_hls(video)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # حذف فایل ویدیو و HLS
        self.delete_video_files(video)
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def convert_to_hls(self, video):
        mp4_file_path = video.video_file.path
        hls_output_dir = os.path.join('media', 'hls', str(video.id))
        os.makedirs(hls_output_dir, exist_ok=True)
        hls_output_path = os.path.join(hls_output_dir, 'output.m3u8')

        # تبدیل ویدیو به HLS
        ffmpeg.input(mp4_file_path).output(
            hls_output_path,
            format='hls',
            hls_time=10,
            hls_playlist_type='vod'
        ).run()

        # ذخیره لینک HLS در مدل
        video.hls_link = f'/media/hls/{video.id}/output.m3u8'
        video.save()

    def delete_video_files(self, video):
        # حذف فایل ویدیوی MP4
        if video.video_file:
            if os.path.isfile(video.video_file.path):
                os.remove(video.video_file.path)

        # حذف فایل HLS
        hls_output_dir = os.path.join('media', 'hls', str(video.id))
        if os.path.isdir(hls_output_dir):
            for filename in os.listdir(hls_output_dir):
                file_path = os.path.join(hls_output_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(hls_output_dir)


