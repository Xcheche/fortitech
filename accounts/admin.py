from django.contrib import admin

from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff')
    ordering = ('-created_at','updated_at',)

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(PendingUser)
