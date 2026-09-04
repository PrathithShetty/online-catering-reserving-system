from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.cart_item_remove, name='cart_item_remove'),
    path('checkout/', views.checkout, name='checkout'),

    path('my-orders/', views.my_orders, name='my_orders'),
    path('my-orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('my-orders/<int:pk>/cancel/', views.order_cancel, name='order_cancel'),
    path('my-orders/<int:order_pk>/review/<int:package_pk>/', views.add_review, name='add_review'),

    # Admin dashboard
    path('dashboard/orders/', views.order_manage_list, name='order_manage_list'),
    path('dashboard/orders/<int:pk>/update-status/', views.order_update_status, name='order_update_status'),
]
