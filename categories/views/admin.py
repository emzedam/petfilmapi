from django.shortcuts import render


import os
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from categories.permissions import IsAuthenticated
from categories.models import Category
from categories.serializers import (
    CategoryListSerializer,
    CategoryDetailSerializer,
    CategoryCreateSerializer,
    CategoryUpdateSerializer
)

class AdminCategoryViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = CategoryListSerializer

    
    def list(self, request):
        queryset = Category.get_root_nodes()
        serializer = CategoryListSerializer(queryset, many=True)
        return Response(serializer.data)

    # دریافت یک دسته‌بندی خاص
    def retrieve(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data)


    # ساخت دسته‌بندی جدید
    def create(self, request):
        serializer = CategoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            parent_id = request.data.get('parent_id', None)
            parent = Category.objects.get(id=parent_id) if parent_id else None
            category = Category.add_root(**serializer.validated_data) if not parent else parent.add_child(**serializer.validated_data)
            return Response(CategoryDetailSerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # بروزرسانی دسته‌بندی
    def update(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        # حذف تصویر قبلی
        # self.remove_cat_image(category)
        
        serializer = CategoryUpdateSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # حذف دسته‌بندی
    def destroy(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        # حذف تصویر دسته‌بندی قبل از حذف شیء
        # self.remove_cat_image(category)
        
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
     # متد حذف تصویر دسته‌بندی
    def remove_cat_image(self, category):
        if category.image:  # فرض می‌کنیم فیلدی به نام image برای دسته‌بندی دارید
            image_path = category.image.path
            if os.path.exists(image_path):
                os.remove(image_path)

