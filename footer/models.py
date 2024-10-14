from django.db import models


# مدل برای توضیحات درباره سایت
class FooterDescription(models.Model):
    description = models.TextField(verbose_name="توضیحات")  # متن توضیح درباره سایت

    def __str__(self):
        return "توضیحات پاورقی"

    class Meta:
        verbose_name = "توضیحات پاورقی"
        verbose_name_plural = "توضیحات پاورقی"
# مدل برای لینک‌های فوتر
class FooterLink(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان")  # عنوان لینک
    url = models.URLField(verbose_name="لینک")  # آدرس لینک

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "لینک های پاورقی"
        verbose_name_plural = "لینک های پاورقی"