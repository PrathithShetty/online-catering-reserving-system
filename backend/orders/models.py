from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from catering.models import CateringPackage


class Cart(models.Model):
    customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        return sum((item.subtotal for item in self.items.all()), Decimal('0.00'))

    def __str__(self):
        return f'Cart of {self.customer.username}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    package = models.ForeignKey(CateringPackage, on_delete=models.CASCADE)
    event_date = models.DateField()
    guest_count = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']

    @property
    def subtotal(self):
        return self.package.price_per_plate * self.guest_count

    def __str__(self):
        return f'{self.package.name} x {self.guest_count} guests'


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Approval'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        REJECTED = 'REJECTED', 'Rejected'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    delivery_address = models.TextField()
    contact_phone = models.CharField(max_length=15)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def recalculate_total(self):
        total = sum((item.subtotal for item in self.items.all()), Decimal('0.00'))
        self.total_amount = total
        self.save(update_fields=['total_amount'])

    def __str__(self):
        return f'Order #{self.pk} - {self.customer.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    package = models.ForeignKey(CateringPackage, on_delete=models.PROTECT, related_name='order_items')
    package_name = models.CharField(max_length=150)
    price_per_plate = models.DecimalField(max_digits=8, decimal_places=2)
    event_date = models.DateField()
    guest_count = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True)

    @property
    def subtotal(self):
        return self.price_per_plate * self.guest_count

    def __str__(self):
        return f'{self.package_name} x {self.guest_count} guests'


class Review(models.Model):
    package = models.ForeignKey(CateringPackage, related_name='reviews', on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('package', 'customer', 'order')

    def __str__(self):
        return f'{self.package.name} - {self.rating} stars by {self.customer.username}'
