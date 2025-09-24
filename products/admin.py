from django.contrib import admin
from .models import Category,Product,File

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["parent","title","is_enabled","created_time"]
    list_filter = ["parent","is_enabled"]
    search_fields = ["title"]

class FileInlineAdmin(admin.StackedInline):
    model = File
    fields = ["file","file_type","title","is_enabled"]
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title","created_time","is_enabled"]
    list_filter = ["is_enabled"]
    search_fields = ["title"]
    filter_horizontal = ["categories"]
    inlines = [FileInlineAdmin]