from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import UserProfile
from products.models import Product
from orders.models import Order
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification


# ─── helpers ────────────────────────────────────────────────────────────────

def _is_admin(user):
    return user.is_superuser or user.is_staff


def _send(subject, body, recipients):
    """Send email; returns (ok, info_string)."""
    if not recipients:
        return False, "No recipients with email addresses."
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
        return True, f"Email sent to {len(recipients)} recipient(s)."
    except Exception as exc:
        return False, str(exc)


# ─── routing ────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    """Smart router — sends each user to the right dashboard."""
    user = request.user
    if _is_admin(user):
        return redirect('admin_dashboard')
    if hasattr(user, 'profile'):
        if user.profile.is_supplier():
            return redirect('supplier_dashboard')
        elif user.profile.is_buyer():
            return redirect('buyer_dashboard')
    return redirect('login')


# ─── admin ──────────────────────────────────────────────────────────────────

@login_required
def admin_dashboard(request):
    """Admin sees full platform overview."""
    if not _is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    context = {
        'total_users':       User.objects.count(),
        'total_suppliers':   UserProfile.objects.filter(role='supplier').count(),
        'total_buyers':      UserProfile.objects.filter(role='buyer').count(),
        'pending_suppliers': UserProfile.objects.filter(role='supplier', is_approved=False),
        'total_products':    Product.objects.count(),
        'total_orders':      Order.objects.count(),
        'recent_orders':     Order.objects.select_related('buyer', 'product').order_by('-placed_at')[:10],
        'all_suppliers':     UserProfile.objects.filter(role='supplier').select_related('user'),
        'all_buyers':        UserProfile.objects.filter(role='buyer').select_related('user'),
        'order_statuses':    Order.STATUS_CHOICES,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


# ─── approval ───────────────────────────────────────────────────────────────

@login_required
def approve_supplier(request, user_id):
    """Admin approves a supplier and sends an email notification."""
    if not _is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    profile = get_object_or_404(UserProfile, user_id=user_id, role='supplier')
    profile.is_approved = True
    profile.save()

    name = profile.user.first_name or profile.user.username
    body = (
        f"Hello {name},\n\n"
        "🎉 Great news! Your supplier account on PartLink has been APPROVED by the admin.\n\n"
        "You can now log in, start listing your products and start receiving orders.\n\n"
        "Login at: http://127.0.0.1:8000/accounts/login/\n\n"
        "Thank you,\nPartLink Team"
    )
    ok, info = _send("✅ Your Supplier Account is Approved — PartLink", body,
                     [profile.user.email] if profile.user.email else [])
    if ok:
        messages.success(request, f'Supplier "{profile.user.username}" approved & notified via email.')
    else:
        messages.success(request, f'Supplier "{profile.user.username}" approved. (Email: {info})')
    return redirect('admin_dashboard')


@login_required
def reject_supplier(request, user_id):
    """Admin rejects/revokes a supplier."""
    if not _is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    profile = get_object_or_404(UserProfile, user_id=user_id, role='supplier')
    profile.is_approved = False
    profile.save()
    messages.warning(request, f'Supplier "{profile.user.username}" has been rejected.')
    return redirect('admin_dashboard')


# ─── notify individual supplier ─────────────────────────────────────────────

@login_required
def notify_supplier(request, user_id):
    """Admin sends a custom notification to a specific supplier."""
    if not _is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    if request.method != 'POST':
        return redirect('admin_dashboard')

    profile = get_object_or_404(UserProfile, user_id=user_id, role='supplier')
    subject = request.POST.get('subject', '').strip() or 'Message from PartLink Admin'
    message = request.POST.get('message', '').strip()

    if not message:
        messages.error(request, 'Message body cannot be empty.')
        return redirect('admin_dashboard')

    name = profile.user.first_name or profile.user.username
    body = f"Hello {name},\n\n{message}\n\nRegards,\nPartLink Admin Team"
    
    # Create in-app notification
    Notification.objects.create(user=profile.user, subject=subject, message=message)
    
    ok, info = _send(subject, body,
                     [profile.user.email] if profile.user.email else [])
    if ok:
        messages.success(request, f'📧 Notification sent to supplier "{profile.user.username}".')
    else:
        messages.error(request, f'Failed to notify supplier "{profile.user.username}": {info}')
    return redirect('admin_dashboard')


# ─── notify individual buyer ────────────────────────────────────────────────

@login_required
def notify_buyer(request, user_id):
    """Admin sends a custom notification to a specific buyer."""
    if not _is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    if request.method != 'POST':
        return redirect('admin_dashboard')

    profile = get_object_or_404(UserProfile, user_id=user_id, role='buyer')
    subject = request.POST.get('subject', '').strip() or 'Message from PartLink Admin'
    message = request.POST.get('message', '').strip()

    if not message:
        messages.error(request, 'Message body cannot be empty.')
        return redirect('admin_dashboard')

    name = profile.user.first_name or profile.user.username
    body = f"Hello {name},\n\n{message}\n\nRegards,\nPartLink Admin Team"
    
    # Create in-app notification
    Notification.objects.create(user=profile.user, subject=subject, message=message)

    ok, info = _send(subject, body,
                     [profile.user.email] if profile.user.email else [])
    if ok:
        messages.success(request, f'📧 Notification sent to buyer "{profile.user.username}".')
    else:
        messages.error(request, f'Failed to notify buyer "{profile.user.username}": {info}')
    return redirect('admin_dashboard')


# ─── broadcast notifications ────────────────────────────────────────────────

@login_required
def notify_all_suppliers(request):
    """Admin broadcasts a notification to ALL approved suppliers."""
    if not _is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    if request.method != 'POST':
        return redirect('admin_dashboard')

    subject = request.POST.get('subject', '').strip() or 'Important Update from PartLink'
    message = request.POST.get('message', '').strip()

    if not message:
        messages.error(request, 'Broadcast message cannot be empty.')
        return redirect('admin_dashboard')

    profiles = UserProfile.objects.filter(role='supplier', is_approved=True)
    emails = list(profiles.exclude(user__email='').values_list('user__email', flat=True))
    
    body = f"Dear Supplier,\n\n{message}\n\nRegards,\nPartLink Admin Team"
    ok, info = _send(subject, body, emails)

    # Create in-app notifications
    notifications = [Notification(user=p.user, subject=subject, message=message) for p in profiles]
    Notification.objects.bulk_create(notifications)

    if ok or notifications:
        messages.success(request, f'📢 Broadcast sent to {profiles.count()} approved supplier(s).')
    else:
        messages.error(request, f'Broadcast failed: {info}')
    return redirect('admin_dashboard')


@login_required
def notify_all_buyers(request):
    """Admin broadcasts a notification to ALL buyers."""
    if not _is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    if request.method != 'POST':
        return redirect('admin_dashboard')

    subject = request.POST.get('subject', '').strip() or 'Important Update from PartLink'
    message = request.POST.get('message', '').strip()

    if not message:
        messages.error(request, 'Broadcast message cannot be empty.')
        return redirect('admin_dashboard')

    profiles = UserProfile.objects.filter(role='buyer')
    emails = list(profiles.exclude(user__email='').values_list('user__email', flat=True))
    
    body = f"Dear Buyer,\n\n{message}\n\nRegards,\nPartLink Admin Team"
    ok, info = _send(subject, body, emails)

    # Create in-app notifications
    notifications = [Notification(user=p.user, subject=subject, message=message) for p in profiles]
    Notification.objects.bulk_create(notifications)

    if ok or notifications:
        messages.success(request, f'📢 Broadcast sent to {profiles.count()} buyer(s).')
    else:
        messages.error(request, f'Broadcast failed: {info}')
    return redirect('admin_dashboard')


# ─── order status update ─────────────────────────────────────────────────────

@login_required
def update_order_status(request, order_id):
    """Admin manually updates an order's status and notifies both buyer and supplier."""
    if not _is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    if request.method != 'POST':
        return redirect('admin_dashboard')

    order = get_object_or_404(Order, pk=order_id)
    new_status = request.POST.get('status', '').strip()
    valid_statuses = [s[0] for s in Order.STATUS_CHOICES]

    if new_status not in valid_statuses:
        messages.error(request, f'Invalid status "{new_status}".')
        return redirect('admin_dashboard')

    old_status = order.get_status_display()
    order.status = new_status
    order.save()
    new_status_display = order.get_status_display()

    # Notify buyer
    buyer_subj = f"Order #{order.id} Status Updated — PartLink"
    buyer_msg_short = f"Your order #{order.id} for «{order.product.name}» has been updated from '{old_status}' to '{new_status_display}'."
    buyer_body = (
        f"Hello {order.buyer.first_name or order.buyer.username},\n\n"
        f"{buyer_msg_short}\n\n"
        "Login to PartLink for more details.\n\nPartLink Team"
    )
    _send(buyer_subj, buyer_body, [order.buyer.email] if order.buyer.email else [])
    Notification.objects.create(user=order.buyer, subject=buyer_subj, message=buyer_msg_short)

    # Notify supplier
    supplier = order.product.supplier
    supplier_subj = f"Order #{order.id} Status Updated — PartLink"
    supplier_msg_short = f"An order for your product «{order.product.name}» has been updated to '{new_status_display}' by admin."
    supplier_body = (
        f"Hello {supplier.first_name or supplier.username},\n\n"
        f"{supplier_msg_short}\n\n"
        "Login to PartLink for more details.\n\nPartLink Team"
    )
    _send(supplier_subj, supplier_body, [supplier.email] if supplier.email else [])
    Notification.objects.create(user=supplier, subject=supplier_subj, message=supplier_msg_short)

    messages.success(request, f'Order #{order.id} status updated to "{new_status_display}" and parties notified.')
    return redirect('admin_dashboard')


# ─── supplier / buyer dashboards ─────────────────────────────────────────────

@login_required
def supplier_dashboard(request):
    """Supplier sees their products and incoming orders."""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_supplier():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    my_products = Product.objects.filter(supplier=request.user)
    my_orders   = Order.objects.filter(product__supplier=request.user).select_related('buyer', 'product')

    context = {
        'total_products':  my_products.count(),
        'active_products': my_products.filter(is_active=True).count(),
        'total_orders':    my_orders.count(),
        'pending_orders':  my_orders.filter(status='pending').count(),
        'recent_orders':   my_orders[:5],
        'low_stock':       my_products.filter(stock_quantity__lte=10),
        'profile':         request.user.profile,
        'notifications':   Notification.objects.filter(user=request.user).order_by('-created_at')[:10],
    }
    return render(request, 'dashboard/supplier_dashboard.html', context)


@login_required
def buyer_dashboard(request):
    """Buyer sees their order history and browsing stats."""
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
        'notifications':    Notification.objects.filter(user=request.user).order_by('-created_at')[:10],
    }
    return render(request, 'dashboard/buyer_dashboard.html', context)
