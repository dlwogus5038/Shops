from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
#from .models import Friend

# Register your models here.
from .models import Shop, Comment

'''
class ProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False
    verbose_name = 'profile'
'''
'''
class FriendInline(admin.StackedInline):
    model = Friend
    max_num = 10
    can_delete = False
    verbose_name = 'Friend'
'''

'''
class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline, ]
'''


admin.site.register(User)
admin.site.register(Shop)
admin.site.register(Comment)
