from django.urls import path
from . import views

urlpatterns = [
    path('',                                    views.dashboard,              name='dashboard'),
    path('admin/',                              views.admin_dashboard,        name='admin_dashboard'),
    path('supplier/',                           views.supplier_dashboard,     name='supplier_dashboard'),
    path('buyer/',                              views.buyer_dashboard,        name='buyer_dashboard'),

    # Supplier approval
    path('approve/<int:user_id>/',             views.approve_supplier,       name='approve_supplier'),
    path('reject/<int:user_id>/',              views.reject_supplier,        name='reject_supplier'),

    # Notify individual users
    path('notify/supplier/<int:user_id>/',     views.notify_supplier,        name='notify_supplier'),
    path('notify/buyer/<int:user_id>/',        views.notify_buyer,           name='notify_buyer'),

    # Broadcast to all
    path('notify/all-suppliers/',              views.notify_all_suppliers,   name='notify_all_suppliers'),
    path('notify/all-buyers/',                 views.notify_all_buyers,      name='notify_all_buyers'),

    # Order management
    path('order/<int:order_id>/status/',       views.update_order_status,    name='update_order_status'),
]
