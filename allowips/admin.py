from django.contrib import admin

# Register your models here.
from .models import AlloweIps

class AlloweIpsAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'is_active', 'created_at']


admin.site.register(AlloweIps , AlloweIpsAdmin)