from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AddRequestSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class AddFavoritesView(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = AddRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # ثبت رابطه در صورت ولید بودن داده‌ها
            return Response({"message": "ویدیو با موفقیت به علاقه مندی ها اضافه شد."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveFavoriteView(APIView):
    def post(self , request):
        pass    