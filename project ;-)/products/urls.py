from django.urls import path
from . import views

urlpatterns = [
    path('',                   views.product_list,         name='product_list'),
    path('<int:pk>/',          views.product_detail,       name='product_detail'),
    path('my/',                views.supplier_product_list, name='supplier_products'),
    path('add/',               views.product_add,          name='product_add'),
    path('<int:pk>/edit/',     views.product_edit,         name='product_edit'),
    path('<int:pk>/delete/',   views.product_delete,       name='product_delete'),
]
