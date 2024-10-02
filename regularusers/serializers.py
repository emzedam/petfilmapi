from rest_framework import serializers
from videos.serializers import VideoSerializer
from .models import (
    User,
    OTPRequest
)

class UserSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True)
    class Meta:
        model = User
        fields = ['phone_number' , 'first_name' , 'last_name' , 'videos']


class RequestOtpSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=50 , allow_null=False)
    channel = serializers.ChoiceField(choices=OTPRequest.OtpChannel.choices)
    

class ResponseOtpRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPRequest
        fields = ['request_id']    
        


class VerifyOtpRequestSerializer(serializers.Serializer):
    request_id = serializers.UUIDField(allow_null= False)   
    password = serializers.CharField(max_length=4 , allow_null=False)
    receiver = serializers.CharField(max_length=64 , allow_null=False)     
    

class ObtainTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128 , allow_null= False)
    refresh = serializers.CharField(max_length=128 , allow_null=False)
    created = serializers.BooleanField()    
    

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'first_name', 'last_name']

    # ولیدیشن برای شماره همراه
    def validate_phone_number(self, value):
        if not value:
            raise serializers.ValidationError("فیلد شماره همراه الزامیست")
        if not value.isdigit():
            raise serializers.ValidationError("شماره همراه باید از نوع عدد باشد.")
        if not value.startswith('0'):
            raise serializers.ValidationError("فرمت شماره همراه اشتباه است . حتما باید با صفر شروع شده باشد.")
        if len(value) != 11:
            raise serializers.ValidationError("شماره همراه اشتباه است.")
        return value

    # ولیدیشن برای نام
    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError("فیلد نام الزامیست")
        if len(value) < 2:
            raise serializers.ValidationError("فیلد نام نباید کمتر از ۲ کاراکتر باشد.")
        if len(value) > 20:
            raise serializers.ValidationError("فیلد نام نمیتواند از ۲۰ کاراکتر بیشتر باشد")
        return value

    # ولیدیشن برای نام خانوادگی
    def validate_last_name(self, value):
        if not value:
            raise serializers.ValidationError("فیلد نام خانوادگی الزامیست")
        if len(value) < 2:
            raise serializers.ValidationError("فیلد نام خانوادگی نباید از ۲ کاراکتر کمتر باشد.")
        if len(value) > 50:
            raise serializers.ValidationError("فیلد نام خانوادگی نباید از ۵۰ کاراکتر بیشتر باشد.")
        return value