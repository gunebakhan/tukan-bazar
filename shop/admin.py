from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'page')


