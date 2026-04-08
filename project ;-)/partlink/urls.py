from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from django.views.generic import TemplateView

urlpatterns = [
    # Django's built-in admin panel at /admin/
    path('admin/', admin.site.urls),

    # Landing Page
    path('', TemplateView.as_view(template_name='landing.html'), name='landing'),

    # All account-related URLs (login, register, logout)
    path('accounts/', include('accounts.urls')),

    # Dashboard URLs (role-based dashboards)
    path('dashboard/', include('dashboard.urls')),

    # Product URLs (supplier manages products)
    path('products/', include('products.urls')),

    # Order URLs (buyer places orders, supplier manages)
    path('orders/', include('orders.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
