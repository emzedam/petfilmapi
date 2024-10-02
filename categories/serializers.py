from rest_framework import serializers
from .models import Category
from videos import serializers as videoserializers

# Serializer برای لیست کردن دسته‌بندی‌ها (نمایش دسته‌بندی‌های ریشه به همراه فرزندان)
class CategoryListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields =  ['id', 'title', 'slug', 'image', 'meta_description', 'meta_keywords', 'is_public', 'children']

    def get_children(self, obj):
        children = obj.get_children()
        return CategoryListSerializer(children, many=True).data


class CategoryWithVideoSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields =  ['id', 'title', 'slug', 'videos']
        
    def get_videos(self, obj):
        # دریافت حداکثر ۶ ویدیو از هر دسته‌بندی که visibility=True باشد
        related_videos = obj.videos.all()[:8]
        return videoserializers.VideoSerializer(related_videos, many=True).data
    

# Serializer برای جزئیات یک دسته‌بندی خاص
class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'meta_description', 'meta_keywords']

# Serializer برای ساخت دسته‌بندی جدید
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Serializer برای بروزرسانی دسته‌بندی
class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'meta_description', 'meta_keywords']