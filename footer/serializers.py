from rest_framework import serializers
from .models import FooterDescription, FooterLink

# سریالایزر برای توضیحات درباره سایت
class FooterDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterDescription
        fields = ['id', 'description']

# سریالایزر برای لینک‌های فوتر
class FooterLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLink
        fields = ['id', 'title', 'url']