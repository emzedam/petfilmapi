# Generated by Django 4.2.16 on 2024-09-29 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
        ('favorites', '0001_initial'),
        ('regularusers', '0002_alter_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='videos',
            field=models.ManyToManyField(through='favorites.UserFavoriteVideo', to='videos.video'),
        ),
    ]
