from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """Form for supplier to add or edit a product"""
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'description', 'material',
            'specifications', 'price_per_unit', 'minimum_order_qty',
            'stock_quantity', 'image', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'specifications': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'price_per_unit': 'Price per Unit (₹)',
            'minimum_order_qty': 'Minimum Order Quantity',
            'stock_quantity': 'Current Stock',
            'is_active': 'Make this product visible to buyers',
        }
