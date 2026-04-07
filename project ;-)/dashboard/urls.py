from django.urls import path
from . import views

urlpatterns = [
    path('',                            views.dashboard,          name='dashboard'),
    path('admin/',                      views.admin_dashboard,    name='admin_dashboard'),
    path('supplier/',                   views.supplier_dashboard, name='supplier_dashboard'),
    path('buyer/',                      views.buyer_dashboard,    name='buyer_dashboard'),
    path('approve/<int:user_id>/',      views.approve_supplier,   name='approve_supplier'),
    path('reject/<int:user_id>/',       views.reject_supplier,    name='reject_supplier'),
]
