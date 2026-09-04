from django.contrib import admin

from .models import Category, CateringPackage, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'food_type', 'is_veg')
    list_filter = ('food_type', 'is_veg')
    search_fields = ('name',)


@admin.register(CateringPackage)
class CateringPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_per_plate', 'min_guests', 'max_guests', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('menu_items',)
