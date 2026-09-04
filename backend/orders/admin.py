from django.contrib import admin

from .models import Cart, CartItem, Order, OrderItem, Review


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('package', 'package_name', 'price_per_plate', 'event_date', 'guest_count')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_amount', 'created_at')
    list_filter = ('status',)
    search_fields = ('customer__username', 'id')
    inlines = [OrderItemInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('package', 'customer', 'rating', 'created_at')
    list_filter = ('rating',)


admin.site.register(Cart)
admin.site.register(CartItem)
