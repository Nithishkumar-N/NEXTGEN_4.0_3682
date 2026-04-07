from django.urls import path
from . import views

urlpatterns = [
    path('place/<int:product_id>/',        views.place_order,          name='place_order'),
    path('my/',                            views.buyer_orders,         name='buyer_orders'),
    path('supplier/',                      views.supplier_orders,      name='supplier_orders'),
    path('<int:order_id>/update-status/',  views.update_order_status,  name='update_order_status'),
    path('<int:order_id>/cancel/',         views.cancel_order,         name='cancel_order'),
]
