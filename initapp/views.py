from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from categories.serializers import (CategoryWithVideoSerializer , CategoryListSerializer)
from videos.serializers import VideoSerializer
from categories.models import Category
from videos.models import Video

class InitializeFrontDataViews(APIView):
    def get(self , request):
        # cover video
        cover_video = Video.objects.filter(is_banner=True)
        video_serializer = VideoSerializer(cover_video , many=True)
        
        # main categories
        main_categories = Category.objects.all().order_by('-id')[:6]
        main_category_serializer = CategoryListSerializer(main_categories , many=True)
        
        # vitrin categories
        categories = Category.objects.filter(visibility=True)
        vitrin_category_serializer = CategoryWithVideoSerializer(categories , many=True)
        

        return Response(data= {
            "cover_video": video_serializer.data,
            "main_categories": main_category_serializer.data,
            "vitrin_categories": vitrin_category_serializer.data    
        } , status=status.HTTP_200_OK)
        
