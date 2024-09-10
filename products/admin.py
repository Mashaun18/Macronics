from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'vendor', 'price', 'category', 'stock', 'created_at', 'updated_at')
    search_fields = ('id', 'name', 'vendor', 'category')
    list_filter = ('created_at', 'updated_at')

admin.site.register(Product, ProductAdmin)