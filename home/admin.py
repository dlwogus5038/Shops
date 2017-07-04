from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile,MyFriend

# Register your models here.
from .models import Shop, Comment

class ProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False
    verbose_name = 'profile'
'''
class FriendInline(admin.StackedInline):
    model = MyFriend
    max_num = 10
    can_delete = False
    verbose_name = 'Friend'
'''
class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline, ]


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Shop)
admin.site.register(Comment)
