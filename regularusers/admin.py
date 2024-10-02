from django.contrib import admin
from .models import (User , OTPRequest)
# Register your models here.


class RegularUserAdmin(admin.ModelAdmin):
    list_display = ['username' , 'is_staff', 'first_name' , 'last_name' , 'phone_number' , 'verified']

admin.site.register(User , RegularUserAdmin)
admin.site.register(OTPRequest)