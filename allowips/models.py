from django.db import models

# Create your models here.

class AlloweIps(models.Model):
    ip_address = models.CharField(max_length=255 , unique=True , verbose_name="آدرس آی پی")
    is_active = models.BooleanField(default=True , verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True , verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="آی پی"
        verbose_name_plural = 'مدیریت آی پی ها'
        db_table = 'allowed_ips'

    def __str__(self):
        return self.ip_address    

