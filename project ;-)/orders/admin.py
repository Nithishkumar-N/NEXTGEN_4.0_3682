from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ['id', 'buyer', 'product', 'quantity', 'total_price', 'status', 'placed_at']
    list_filter   = ['status']
    search_fields = ['buyer__username', 'product__name']
    readonly_fields = ['total_price', 'placed_at', 'updated_at']
