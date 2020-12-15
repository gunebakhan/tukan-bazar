from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'create', 'update')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'create', 'update')


@admin.register(ImageGallery)
class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('image', 'product', 'created', 'updated')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'slug', 'available', 'sold', 'created', 'updated')



