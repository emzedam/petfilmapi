from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AddRequestSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import UserFavoriteVideo
from videos.models import Video



class AddFavoritesView(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = AddRequestSerializer(data=request.data)
        if serializer.is_valid():
            video_id = request.data.get('video_id')
            try:
                video = Video.objects.get(id=video_id)
            except Video.DoesNotExist:
                return Response({"error": "ویدیو یافت نشد!"}, status=status.HTTP_404_NOT_FOUND)

        
            user = request.user
            favoriteObject = UserFavoriteVideo.objects.filter(user=user, video=video)
            if favoriteObject.exists():
                favoriteObject.delete()
                return Response({"message": "ویدیو از علاقه مندی های شما خارج شد"}, status=status.HTTP_200_OK)
            else:     
                UserFavoriteVideo.objects.create(user=user, video=video) 
                return Response({"message": "ویدیو به علاقه مندی های شما اضافه شد"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
