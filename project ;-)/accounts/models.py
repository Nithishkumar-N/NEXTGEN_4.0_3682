from django.db import models
from django.contrib.auth.models import User

# UserProfile extends Django's built-in User model
# Django already gives us: username, email, password, first_name, last_name
# We add: role (supplier/buyer) and approval status for suppliers
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('supplier', 'Supplier'),  # Manufacturer who sells parts
        ('buyer', 'Buyer'),        # Industry that buys parts
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    # Suppliers need admin approval before they can list products
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    def is_supplier(self):
        return self.role == 'supplier'

    def is_buyer(self):
        return self.role == 'buyer'
