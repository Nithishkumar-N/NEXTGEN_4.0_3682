from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import UserProfile
from products.models import Product
from orders.models import Order
from django.core.mail import send_mail
from django.conf import settings


@login_required
def dashboard(request):
    """
    Smart router — sends each user to the right dashboard
    based on their role (admin / supplier / buyer)
    """
    user = request.user

    if user.is_superuser or user.is_staff:
        return redirect('admin_dashboard')

    if hasattr(user, 'profile'):
        if user.profile.is_supplier():
            return redirect('supplier_dashboard')
        elif user.profile.is_buyer():
            return redirect('buyer_dashboard')

    return redirect('login')


@login_required
def admin_dashboard(request):
    """Admin sees full platform overview"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    context = {
        'total_users':     User.objects.count(),
        'total_suppliers': UserProfile.objects.filter(role='supplier').count(),
        'total_buyers':    UserProfile.objects.filter(role='buyer').count(),
        'pending_suppliers': UserProfile.objects.filter(role='supplier', is_approved=False),
        'total_products':  Product.objects.count(),
        'total_orders':    Order.objects.count(),
        'recent_orders':   Order.objects.select_related('buyer', 'product').order_by('-placed_at')[:10],
        'all_suppliers':   UserProfile.objects.filter(role='supplier').select_related('user'),
        'all_buyers':      UserProfile.objects.filter(role='buyer').select_related('user'),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def supplier_dashboard(request):
    """Supplier sees their products and incoming orders"""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_supplier():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    my_products = Product.objects.filter(supplier=request.user)
    my_orders   = Order.objects.filter(product__supplier=request.user).select_related('buyer', 'product')

    context = {
        'total_products':   my_products.count(),
        'active_products':  my_products.filter(is_active=True).count(),
        'total_orders':     my_orders.count(),
        'pending_orders':   my_orders.filter(status='pending').count(),
        'recent_orders':    my_orders[:5],
        'low_stock':        my_products.filter(stock_quantity__lte=10),
        'profile':          request.user.profile,
    }
    return render(request, 'dashboard/supplier_dashboard.html', context)


@login_required
def buyer_dashboard(request):
    """Buyer sees their order history and browsing stats"""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_buyer():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    my_orders = Order.objects.filter(buyer=request.user).select_related('product')
    context = {
        'total_orders':     my_orders.count(),
        'pending_orders':   my_orders.filter(status='pending').count(),
        'delivered_orders': my_orders.filter(status='delivered').count(),
        'recent_orders':    my_orders[:5],
        'total_products':   Product.objects.filter(is_active=True).count(),
        'profile':          request.user.profile,
    }
    return render(request, 'dashboard/buyer_dashboard.html', context)


@login_required
def approve_supplier(request, user_id):
    """Admin approves a supplier"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    profile = get_object_or_404(UserProfile, user_id=user_id, role='supplier')
    profile.is_approved = True
    profile.save()
    
    # Send email notification
    user_email = profile.user.email
    if user_email:
        try:
            send_mail(
                subject='Your Supplier Account is Approved!',
                message=f'Hello {profile.user.first_name or profile.user.username},\n\nGreat news! Your supplier account on PartLink has been approved by the admin. You can now login, start listing your products and receiving orders.\n\nThank you,\nPartLink Team',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )
            messages.success(request, f'Supplier "{profile.user.username}" has been approved and notified via email!')
        except Exception as e:
            messages.success(request, f'Supplier "{profile.user.username}" is approved, but email failed: {str(e)}')
    else:
        messages.success(request, f'Supplier "{profile.user.username}" has been approved! (No email address was provided)')
        
    return redirect('admin_dashboard')


@login_required
def reject_supplier(request, user_id):
    """Admin rejects/revokes a supplier"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    profile = get_object_or_404(UserProfile, user_id=user_id, role='supplier')
    profile.is_approved = False
    profile.save()
    messages.success(request, f'Supplier "{profile.user.username}" has been rejected.')
    return redirect('admin_dashboard')
