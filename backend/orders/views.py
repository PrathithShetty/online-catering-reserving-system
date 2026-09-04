from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required
from catering.models import CateringPackage

from .forms import AddToCartForm, CheckoutForm, ReviewForm
from .models import Cart, CartItem, Order, OrderItem, Review


def _get_cart(user):
    cart, _ = Cart.objects.get_or_create(customer=user)
    return cart


@login_required
def add_to_cart(request, slug):
    package = get_object_or_404(CateringPackage, slug=slug, is_active=True)
    if request.method == 'POST':
        form = AddToCartForm(request.POST, package=package)
        if form.is_valid():
            cart = _get_cart(request.user)
            item = form.save(commit=False)
            item.cart = cart
            item.package = package
            item.save()
            messages.success(request, f'{package.name} added to your cart.')
            return redirect('orders:cart')
    else:
        form = AddToCartForm(package=package)
    return render(request, 'orders/add_to_cart.html', {'form': form, 'package': package})


@login_required
def cart_view(request):
    cart = _get_cart(request.user)
    return render(request, 'orders/cart.html', {'cart': cart})


@login_required
def cart_item_remove(request, pk):
    item = get_object_or_404(CartItem, pk=pk, cart__customer=request.user)
    item.delete()
    messages.info(request, 'Item removed from cart.')
    return redirect('orders:cart')


@login_required
def checkout(request):
    cart = _get_cart(request.user)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('orders:cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.save()

            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    package=cart_item.package,
                    package_name=cart_item.package.name,
                    price_per_plate=cart_item.package.price_per_plate,
                    event_date=cart_item.event_date,
                    guest_count=cart_item.guest_count,
                    special_requests=cart_item.special_requests,
                )
            order.recalculate_total()
            cart.items.all().delete()

            messages.success(request, 'Your booking request has been placed! We will confirm it shortly.')
            return redirect('orders:order_detail', pk=order.pk)
    else:
        initial = {'delivery_address': request.user.address, 'contact_phone': request.user.phone}
        form = CheckoutForm(initial=initial)

    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})


@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).prefetch_related('items')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    if request.user.is_catering_admin:
        order = get_object_or_404(Order, pk=pk)
    else:
        order = get_object_or_404(Order, pk=pk, customer=request.user)
    reviewed_package_ids = set(
        Review.objects.filter(order=order, customer=order.customer).values_list('package_id', flat=True)
    )
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'reviewed_package_ids': reviewed_package_ids,
    })


@login_required
def order_cancel(request, pk):
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    if request.method == 'POST' and order.status == Order.Status.PENDING:
        order.status = Order.Status.CANCELLED
        order.save(update_fields=['status'])
        messages.info(request, f'Order #{order.pk} has been cancelled.')
    return redirect('orders:my_orders')


@login_required
def add_review(request, order_pk, package_pk):
    order = get_object_or_404(Order, pk=order_pk, customer=request.user, status=Order.Status.COMPLETED)
    package = get_object_or_404(CateringPackage, pk=package_pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review, created = Review.objects.update_or_create(
                package=package, customer=request.user, order=order,
                defaults={'rating': form.cleaned_data['rating'], 'comment': form.cleaned_data['comment']},
            )
            messages.success(request, 'Thank you for your review!')
            return redirect('orders:order_detail', pk=order.pk)
    else:
        form = ReviewForm()
    return render(request, 'orders/add_review.html', {'form': form, 'order': order, 'package': package})


# ---------------------------------------------------------------------------
# Admin dashboard: order management
# ---------------------------------------------------------------------------

@admin_required
def order_manage_list(request):
    orders = Order.objects.select_related('customer').prefetch_related('items')
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'orders/dashboard/order_manage_list.html', {
        'orders': orders,
        'status_choices': Order.Status.choices,
        'selected_status': status_filter or '',
    })


@admin_required
def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in Order.Status.values:
            order.status = new_status
            order.save(update_fields=['status'])
            messages.success(request, f'Order #{order.pk} marked as {order.get_status_display()}.')
    return redirect('orders:order_manage_list')
