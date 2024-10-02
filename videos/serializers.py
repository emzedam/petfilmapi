from rest_framework import serializers
from categories import serializers as category_serializers
from categories import models as category_models
from .models import Video

class VideoSerializer(serializers.ModelSerializer):


    category = serializers.PrimaryKeyRelatedField(queryset=category_models.Category.objects.all() , required=False, allow_null=True)
    
    class Meta:
        model = Video
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.category:
            representation['category'] = {
                "id": instance.category.id,
                "title": instance.category.title,
                "image": instance.category.image.url if instance.category.image else None
            }
        return representation
    