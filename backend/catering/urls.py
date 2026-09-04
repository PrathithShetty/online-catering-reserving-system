from django.urls import path

from . import views

app_name = 'catering'

urlpatterns = [
    path('', views.home, name='home'),
    path('packages/', views.package_list, name='package_list'),
    path('packages/<slug:slug>/', views.package_detail, name='package_detail'),
    path('menu/', views.menu, name='menu'),

    # Admin dashboard
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/packages/', views.package_manage_list, name='package_manage_list'),
    path('dashboard/packages/add/', views.package_create, name='package_create'),
    path('dashboard/packages/<int:pk>/edit/', views.package_update, name='package_update'),
    path('dashboard/packages/<int:pk>/delete/', views.package_delete, name='package_delete'),

    path('dashboard/menu-items/', views.menu_item_manage_list, name='menu_item_manage_list'),
    path('dashboard/menu-items/add/', views.menu_item_create, name='menu_item_create'),
    path('dashboard/menu-items/<int:pk>/edit/', views.menu_item_update, name='menu_item_update'),
    path('dashboard/menu-items/<int:pk>/delete/', views.menu_item_delete, name='menu_item_delete'),

    path('dashboard/categories/', views.category_manage_list, name='category_manage_list'),
    path('dashboard/categories/add/', views.category_create, name='category_create'),
    path('dashboard/categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('dashboard/categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
