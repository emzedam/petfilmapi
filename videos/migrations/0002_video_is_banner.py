# Generated by Django 4.2.16 on 2024-09-30 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='is_banner',
            field=models.BooleanField(default=False),
        ),
    ]
