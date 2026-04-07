from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm


def product_list(request):
    """
    Public product catalog — buyers search & browse here.
    Supports search by name, category filter.
    """
    products = Product.objects.filter(is_active=True, stock_quantity__gt=0)
    categories = Category.objects.all()

    # Search functionality
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(material__icontains=query)
        )
    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    })


def product_detail(request, pk):
    """Full detail page for a single product"""
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, 'products/product_detail.html', {'product': product})


@login_required
def supplier_product_list(request):
    """Supplier sees only their own products"""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_supplier():
        messages.error(request, 'Only suppliers can access this page.')
        return redirect('dashboard')

    products = Product.objects.filter(supplier=request.user)
    return render(request, 'products/supplier_products.html', {'products': products})


@login_required
def product_add(request):
    """Supplier adds a new product"""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_supplier():
        messages.error(request, 'Only suppliers can add products.')
        return redirect('dashboard')

    if not request.user.profile.is_approved:
        messages.error(request, 'Your account needs admin approval before you can list products.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.supplier = request.user
            product.save()
            messages.success(request, f'Product "{product.name}" added successfully!')
            return redirect('supplier_products')
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {'form': form, 'action': 'Add'})


@login_required
def product_edit(request, pk):
    """Supplier edits their existing product"""
    product = get_object_or_404(Product, pk=pk, supplier=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('supplier_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {'form': form, 'action': 'Edit', 'product': product})


@login_required
def product_delete(request, pk):
    """Supplier deletes their product"""
    product = get_object_or_404(Product, pk=pk, supplier=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('supplier_products')
    return render(request, 'products/product_confirm_delete.html', {'product': product})
