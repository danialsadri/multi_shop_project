from django.contrib import admin
from .models import *


class InformationInline(admin.StackedInline):
    model = Information
    extra = 0
    classes = ('collapse',)
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount', 'get_image', 'created']
    list_filter = ['created']
    search_fields = ['title', 'description']
    inlines = [InformationInline]


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent']
    search_fields = ['title']
    raw_id_fields = ['parent']
    prepopulated_fields = {'slug': ['title']}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'active']
    list_filter = ['created', 'active']
    search_fields = ['name', 'description']
    raw_id_fields = ['product']
    ordering = ['created']
    list_editable = ['active']
