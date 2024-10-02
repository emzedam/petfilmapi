from django.db import models
from treebeard.mp_tree import MP_Node
from libs.slug_generator import slugify
from libs.hash_category_images import hashed_upload_path

class Category(MP_Node):
    title = models.CharField(max_length=255 , verbose_name="عنوان" , db_index=True)
    slug =  models.SlugField(unique=True, blank=True , verbose_name="اسلاگ")
    image = models.ImageField(upload_to=hashed_upload_path, blank=True, null=True , verbose_name="کاور")
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    is_public  = models.BooleanField(default=True , verbose_name="وضعیت")
    visibility = models.BooleanField(default=False , verbose_name="نمایش در صفحه اصلی")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True)

    node_order_by = ['title']

    def __str__(self):
        return self.title
        


    class Meta:
        verbose_name="دسته بندی"
        verbose_name_plural = 'مدیریت دسته بندی ها'
        db_table = 'categories'


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

            unique_slug = self.slug
            num = 1
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{self.slug}-{num}'
                num += 1
            self.slug = unique_slug
    
        super().save(*args, **kwargs)