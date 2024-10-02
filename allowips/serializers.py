from rest_framework import serializers
from .models import AlloweIps

class AllowedIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlloweIps
        fields = ('id', 'ip_address', 'is_active')  # fields to be serialized