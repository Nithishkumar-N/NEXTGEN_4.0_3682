from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    """Represents a buyer's order for a product"""

    STATUS_CHOICES = [
        ('pending',   'Pending'),        # Just placed by buyer
        ('accepted',  'Accepted'),       # Supplier accepted
        ('rejected',  'Rejected'),       # Supplier rejected
        ('shipped',   'Shipped'),        # Supplier shipped it
        ('delivered', 'Delivered'),      # Buyer confirmed delivery
        ('cancelled', 'Cancelled'),      # Buyer cancelled
    ]

    buyer    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Delivery address for this specific order
    delivery_address = models.TextField()
    notes = models.TextField(blank=True, help_text="Any special instructions")

    # Timestamps
    placed_at   = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.product.name} by {self.buyer.username}"

    def save(self, *args, **kwargs):
        # Auto-calculate total price before saving
        self.total_price = self.product.price_per_unit * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-placed_at']  # Newest orders first
