from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, MyBooks

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_profile_picture')

    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.profile_picture.url)
        return None
    
    display_profile_picture.short_description = 'Profile Picture Preview'

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(MyBooks)