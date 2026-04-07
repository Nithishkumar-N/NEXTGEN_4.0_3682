from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['name', 'description']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name', 'supplier', 'category', 'price_per_unit', 'stock_quantity', 'is_active']
    list_filter   = ['is_active', 'category']
    search_fields = ['name', 'supplier__username', 'material']
