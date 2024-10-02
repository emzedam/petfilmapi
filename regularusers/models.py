from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from videos.models import Video
import uuid
import random
import string

# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=15 , null=True , blank=True, verbose_name="شماره موبایل")  # شماره موبایل کاربر
    first_name = models.CharField(max_length=50, blank=True, null=True , verbose_name="نام")  # نام
    last_name = models.CharField(max_length=50, blank=True, null=True , verbose_name="نام خانوادگی")  # نام خانوادگی
    date_joined = models.DateTimeField(auto_now_add=True)  # تاریخ عضویت
    is_active = models.BooleanField(default=True)  # آیا حساب کاربر فعال است یا نه
    verified = models.BooleanField(default=False , verbose_name="وضعیت اکانت")  # آیا کاربر احراز هویت شده است یا نه
    videos = models.ManyToManyField('videos.Video', through='favorites.UserFavoriteVideo')

    def __str__(self):
        return f'{self.phone_number} - {self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name="کاربران سایت"
        verbose_name_plural = 'مدیریت کاربران سایت'
        db_table = 'users'
        



class OtpRequestQuerySet(models.QuerySet):
    def is_verify(self, data):
        current_time = timezone.now()
        return self.filter(
            receiver=data['receiver'],
            password=data['password'],
            request_id=data['request_id'],
            created__lt=current_time,
            created__gt=current_time-timedelta(seconds=120)
        ).exists()
def generate_otp():
    rand = random.SystemRandom()
    digits = rand.choices(string.digits , k=4)
    return ''.join(digits)

class OtpRequestManager(models.Manager):
    
    def get_queryset(self):
        return OtpRequestQuerySet(self.model , self._db)
    
    def is_verify(self , data):
        return self.get_queryset().is_verify(data)
    
    def generate(self , data):
        otp = self.model(channel=data['channel'] , receiver=data['receiver'])
        otp.save(using=self._db)
        return otp

class OTPRequest(models.Model):
    
    class OtpChannel(models.TextChoices):
        PHONE = 'Phone'
        EMAIL = 'E-Mail'
        
    
    request_id = models.UUIDField(primary_key=True , editable=False, default=uuid.uuid4)
    channel = models.CharField(max_length=10 , choices=OtpChannel.choices , default=OtpChannel.PHONE)
    receiver = models.CharField(max_length=50)
    password = models.CharField(max_length=4 , default=generate_otp)
    created = models.DateTimeField(auto_now_add=True , editable=False)
    
    objects = OtpRequestManager()
    
    class Meta:
        verbose_name="درخواست های otp"
        verbose_name_plural = "مدیریت درخواست های otp"
        db_table = 'otp_requests'
        


        