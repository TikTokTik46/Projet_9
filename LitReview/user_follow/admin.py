from django.contrib import admin

# Register your models here.

from .models import UserFollow

class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')

admin.site.register(UserFollow, UserFollowAdmin)
