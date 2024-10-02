
from rest_framework import serializers
from videos.models import Video
from .models import UserFavoriteVideo
from django.contrib.auth import get_user_model

User = get_user_model()

class AddRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    video_id = serializers.IntegerField()
    
    def validate(self, data):
        user_id = data.get('user_id')
        video_id = data.get('video_id')

        # بررسی وجود کاربر
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("کاربر یافت نشد.")

        # بررسی وجود ویدیو
        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            raise serializers.ValidationError("ویدیو یافت نشد.")

        # بررسی اینکه رابطه بین کاربر و ویدیو قبلاً وجود نداشته باشد
        if UserFavoriteVideo.objects.filter(user=user, video=video).exists():
            raise serializers.ValidationError("این ویدیو قبلاً به علاقه ها اضافه شده.")

        return data

    
    def create(self, validated_data):
        # ثبت رابطه جدید در جدول UserFavoriteVideo
        user = User.objects.get(id=validated_data['user_id'])
        video = Video.objects.get(id=validated_data['video_id'])

        user_video = UserFavoriteVideo.objects.create(user=user, video=video)
        return user_video