from django.contrib import admin
from .models import Video
import os
import ffmpeg
import hashlib
from django.utils.safestring import mark_safe

class VideoAdmin(admin.ModelAdmin):
    list_display = ['cover_display' , 'title_fa', 'title_en' , 'created_at', 'category', 'hls_link' , 'is_banner']
    search_fields = ('title_fa', 'title_en')
    readonly_fields = ('slug', 'hls_link')

    def save_model(self, request, obj, form, change):
        if change:
             # اگر فایل جدید ویدیو آپلود شده باشد
            if 'video_file' in form.changed_data:
                # فایل ویدیوی قبلی حذف شود
                self.delete_media_files(obj)

            # اگر فایل کاور جدید آپلود شده باشد
            if 'cover' in form.changed_data:
                # فایل کاور قبلی حذف شود
                self.delete_cover_file(obj)

        if obj.is_banner:
            existing_banner = Video.objects.filter(is_banner=True).exclude(id=obj.id).first()
            if existing_banner:
                existing_banner.is_banner = False
                existing_banner.save()


           
            
            
        super().save_model(request, obj, form, change)
        
        if 'video_file' in form.changed_data:
            self.convert_to_hls(obj)
        
        

    def delete_model(self, request, obj):
        self.delete_cover_file(obj)
        self.delete_video_file(obj)
        
        super().delete_model(request, obj)


    def delete_queryset(self, request, queryset):
        for video in queryset:
            self.delete_cover_file(video)
            self.delete_video_file(video)

        queryset.delete()

    def delete_cover_file(self , video):
        if video.cover:
            cover_file_path = video.cover.path
            if os.path.exists(cover_file_path):
                os.remove(cover_file_path)
                
    def delete_video_file(self , video):
        if video.video_file:
            mp4_file_path = video.video_file.path
            if os.path.exists(mp4_file_path):
                os.remove(mp4_file_path)
                
        hls_output_dir = os.path.join('media', 'hls', str(video.id))
        
        if os.path.exists(hls_output_dir):
            for root, dirs, files in os.walk(hls_output_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(hls_output_dir)        
                
    def convert_to_hls(self, video):
        mp4_file_path = video.video_file.path
        hls_output_dir = os.path.join('media', 'hls', str(video.id))
        os.makedirs(hls_output_dir, exist_ok=True)
        
        hashed_name = hashlib.md5(video.video_file.name.encode('utf-8')).hexdigest()
        hls_output_path = os.path.join(hls_output_dir, f'{hashed_name}.m3u8')
        

        # تبدیل ویدیو به HLS
        ffmpeg.input(mp4_file_path).output(
            hls_output_path,
            format='hls',
            hls_time=10,
            hls_playlist_type='vod'
        ).run()

        # ذخیره لینک HLS در مدل
        video.hls_link = f'/media/hls/{video.id}/{hashed_name}.m3u8'
        video.save()

    def cover_display(self, obj):
        if obj.cover:
            return mark_safe(f'<img src="{obj.cover.url}" style="width: 50px; height: 50px; object-fit:cover;" />')
        return '-'
    cover_display.short_description = 'کاور'

admin.site.register(Video, VideoAdmin)