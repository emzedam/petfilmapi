from django.db import models
from categories.models import Category
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import FileExtensionValidator
from libs.slug_generator import slugify
from libs.hash_video_covers import hashed_upload_path

class Video(models.Model):
    title_fa = models.CharField(max_length=255, verbose_name="عنوان فارسی")
    title_en = models.CharField(max_length=255, verbose_name="عنوان انگلیسی" , null=True)
    description = RichTextUploadingField(verbose_name="توضیحات")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='mp4/' , verbose_name="فایل ویدیو", validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    cover = models.ImageField(upload_to=hashed_upload_path, blank=True, null=True , verbose_name="کاور" , validators=[FileExtensionValidator(allowed_extensions=['jpg' , 'jpeg' , 'png' , 'webp'])])
    hls_link = models.CharField(max_length=255, blank=True, null=True , verbose_name="لینک hls")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='videos' , verbose_name="دسته بندی")
    is_banner = models.BooleanField(default=False , verbose_name="نمایش در بالای صفحه اصلی")
    created_at = models.DateTimeField(auto_now_add=True , verbose_name="تاریخ آپلود")
    updated_at = models.DateTimeField(auto_now=True)

    # seo
    keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name="کلمات کلیدی (با علامت , جدا کنید)")
    seo_description = models.TextField(blank=True, null=True, verbose_name="توضیحات SEO")
    release_year = models.PositiveIntegerField(verbose_name="سال انتشار", null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name="آدرس قابل خواندن", null=True, blank=True)


    class Meta:
        verbose_name="ویدیو"
        verbose_name_plural = 'مدیریت ویدیو ها'
        db_table = 'videos'

    def __str__(self):
        return self.title_fa
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_fa)

            unique_slug = self.slug
            num = 1
            while Video.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{self.slug}-{num}'
                num += 1
            self.slug = unique_slug
    
        super().save(*args, **kwargs)
    
    