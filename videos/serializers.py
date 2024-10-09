from rest_framework import serializers
from categories import serializers as category_serializers
from categories import models as category_models
from .models import Video
import jdatetime

class VideoSerializer(serializers.ModelSerializer):


    category = serializers.PrimaryKeyRelatedField(queryset=category_models.Category.objects.all() , required=False, allow_null=True)
    related_videos = serializers.SerializerMethodField()
    created_at_formatted = serializers.SerializerMethodField()


    class Meta:
        model = Video
        fields = [
            "id",
            "category",
            "title_fa",
            "title_en",
            "description",
            "uploaded_at",
            "video_file",
            "cover",
            "hls_link",
            "is_banner",
            "created_at",
            "created_at_formatted",
            "updated_at",
            "keywords",
            "seo_description",
            "release_year",
            "slug",
            "related_videos"
        ]
        
    def get_related_videos(self, obj):
        # گرفتن ویدیوهای مرتبط از context
        related_videos = self.context.get('related_videos', [])
        return VideoSerializer(related_videos, many=True).data    
        
    def get_created_at_formatted(self, obj):
        # تبدیل تاریخ میلادی به شمسی
        gregorian_date = obj.created_at
        jalali_date = jdatetime.datetime.fromgregorian(datetime=gregorian_date)


        months_persian = {
            'Farvardin': 'فروردین',
            'Ordibehesht': 'اردیبهشت',
            'Khordad': 'خرداد',
            'Tir': 'تیر',
            'Mordad': 'مرداد',
            'Shahrivar': 'شهریور',
            'Mehr': 'مهر',
            'Aban': 'آبان',
            'Azar': 'آذر',
            'Dey': 'دی',
            'Bahman': 'بهمن',
            'Esfand': 'اسفند'
        }

        month_english = jalali_date.strftime('%B')
        
        month_persian = months_persian.get(month_english, month_english)

        return f'{jalali_date.year} {month_persian} {jalali_date.day}'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.category:
            representation['category'] = {
                "id": instance.category.id,
                "title": instance.category.title,
                "slug": instance.category.slug,
                "image": instance.category.image.url if instance.category.image else None
            }
        return representation
    