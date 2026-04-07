from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Categories like: Bolts, Gaskets, Bearings, etc."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    """A small part/product that a supplier lists for sale"""
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=200)
    description = models.TextField()
    material = models.CharField(max_length=100, blank=True, help_text="e.g. Stainless Steel, Aluminium")
    specifications = models.TextField(blank=True, help_text="Dimensions, tolerances, etc.")

    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in INR")
    minimum_order_qty = models.PositiveIntegerField(default=1, help_text="Minimum pieces per order")
    stock_quantity = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to='products/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.supplier.username}"

    def is_in_stock(self):
        return self.stock_quantity > 0
