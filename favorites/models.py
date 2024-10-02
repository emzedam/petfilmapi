from django.db import models
from django.contrib.auth import get_user_model
from videos.models import Video

# Create your models here.

User = get_user_model()
class UserFavoriteVideo(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE , null=False , blank=False , related_name="user_favorites")
    video   = models.ForeignKey(Video , on_delete=models.CASCADE , null=False, blank=False , related_name="videos")
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.video.title_fa}"
    
    class Meta:
        verbose_name="علاقه مندی ها"
        verbose_name_plural = 'مدیریت علاقه مندی ها'
        db_table = 'favorites'