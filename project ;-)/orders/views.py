from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Order


@login_required
def place_order(request, product_id):
    """Buyer places a new order for a product"""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_buyer():
        messages.error(request, 'Only buyers can place orders.')
        return redirect('product_list')

    product = get_object_or_404(Product, pk=product_id, is_active=True)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        delivery_address = request.POST.get('delivery_address', '')
        notes = request.POST.get('notes', '')

        # Validate quantity
        if quantity < product.minimum_order_qty:
            messages.error(request, f'Minimum order quantity is {product.minimum_order_qty} units.')
            return redirect('product_detail', pk=product_id)

        if quantity > product.stock_quantity:
            messages.error(request, f'Only {product.stock_quantity} units available in stock.')
            return redirect('product_detail', pk=product_id)

        if not delivery_address.strip():
            messages.error(request, 'Please provide a delivery address.')
            return redirect('product_detail', pk=product_id)

        # Create the order
        order = Order.objects.create(
            buyer=request.user,
            product=product,
            quantity=quantity,
            delivery_address=delivery_address,
            notes=notes,
        )
        messages.success(request, f'Order #{order.pk} placed successfully! Waiting for supplier confirmation.')
        return redirect('buyer_orders')

    return render(request, 'orders/place_order.html', {'product': product})


@login_required
def buyer_orders(request):
    """Buyer sees all their orders and tracks status"""
    orders = Order.objects.filter(buyer=request.user).select_related('product')
    return render(request, 'orders/buyer_orders.html', {'orders': orders})


@login_required
def supplier_orders(request):
    """Supplier sees all orders for their products"""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_supplier():
        messages.error(request, 'Only suppliers can access this page.')
        return redirect('dashboard')

    orders = Order.objects.filter(product__supplier=request.user).select_related('product', 'buyer')
    return render(request, 'orders/supplier_orders.html', {'orders': orders})


@login_required
def update_order_status(request, order_id):
    """Supplier accepts/rejects/ships an order"""
    order = get_object_or_404(Order, pk=order_id, product__supplier=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = ['accepted', 'rejected', 'shipped', 'delivered']
        if new_status in valid_statuses:
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.pk} marked as {new_status}.')
        else:
            messages.error(request, 'Invalid status.')
    return redirect('supplier_orders')


@login_required
def cancel_order(request, order_id):
    """Buyer cancels a pending order"""
    order = get_object_or_404(Order, pk=order_id, buyer=request.user)

    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Order #{order.pk} has been cancelled.')
    else:
        messages.error(request, 'Only pending orders can be cancelled.')
    return redirect('buyer_orders')
