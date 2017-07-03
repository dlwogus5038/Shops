from django.contrib import admin

# Register your models here.
from .models import Shop, Comment

admin.site.register(Shop)
admin.site.register(Comment)
