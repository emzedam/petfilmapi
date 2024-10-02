from django.utils.safestring import mark_safe
from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import Category
from django.core.files.storage import default_storage


class CategoryAdmin(TreeAdmin):
    list_display = ['title', 'image_display' , 'slug' , 'video_count' , 'visibility']
    search_fields = ['title']
    readonly_fields = ('slug',)
    
    form = movenodeform_factory(Category)

    def image_display(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 50px; height: 50px; object-fit:cover;" />')
        return '-'

    
    def video_count(self, obj):
        return obj.videos.count()
    
    # multiple object delete
    def delete_queryset(self, request, queryset):
        for category in queryset:
            self.delete_media_files(category)

        queryset.delete()
        
    # one object delete 
    def delete_model(self, request, obj):
        self.delete_media_files(obj)
        
        super().delete_model(request, obj)

    def delete_media_files(self, category):
        if category.image and default_storage.exists(category.image.path):
            default_storage.delete(category.image.path)
 
    
    image_display.short_description = 'کاور'
    video_count.short_description = "تعداد ویدیو"

admin.site.site_header = "مدیریت پت فیلم | پت و من"
admin.site.site_title = "پت فیلم"
admin.site.index_title = "خوش آمدید به پنل مدیریت"

admin.site.register(Category, CategoryAdmin)