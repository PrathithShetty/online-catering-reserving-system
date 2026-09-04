from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required

from .forms import CateringPackageForm, CategoryForm, MenuItemForm
from .models import Category, CateringPackage, MenuItem


def home(request):
    categories = Category.objects.all()
    featured_packages = CateringPackage.objects.filter(is_active=True).select_related('category')[:6]
    return render(request, 'catering/home.html', {
        'categories': categories,
        'featured_packages': featured_packages,
    })


def package_list(request):
    packages = CateringPackage.objects.filter(is_active=True).select_related('category')

    category_slug = request.GET.get('category')
    if category_slug:
        packages = packages.filter(category__slug=category_slug)

    query = request.GET.get('q')
    if query:
        packages = packages.filter(Q(name__icontains=query) | Q(description__icontains=query))

    paginator = Paginator(packages, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'catering/package_list.html', {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'selected_category': category_slug,
        'query': query or '',
    })


def package_detail(request, slug):
    package = get_object_or_404(CateringPackage.objects.select_related('category'), slug=slug, is_active=True)
    reviews = package.reviews.select_related('customer').order_by('-created_at')
    return render(request, 'catering/package_detail.html', {
        'package': package,
        'reviews': reviews,
    })


# A hero photo for a handful of menu sections — purely editorial, so it lives
# here rather than as a per-dish image (the real menu boards use one photo
# per section, not one per item).
MENU_SECTION_IMAGES = {
    'Idly & Vada': 'img/rasaganga/food2.jpg',
    'Dosa Varieties': 'img/rasaganga/food4.jpg',
    'Thali & Meals': 'img/rasaganga/food5.jpg',
}


def menu(request):
    items = MenuItem.objects.all().order_by('section', 'food_type', 'name')

    sections = {}
    for item in items:
        sections.setdefault(item.section or 'More', []).append(item)

    section_order = [
        'Idly & Vada', 'Dosa Varieties', 'Chaat & Street Food', 'Indo-Chinese',
        'Thali & Meals', 'Sweets', 'Beverages & Juices',
    ]
    ordered_sections = [
        {'name': name, 'items': sections[name], 'image': MENU_SECTION_IMAGES.get(name)}
        for name in section_order if name in sections
    ]
    for name, section_items in sections.items():
        if name not in section_order:
            ordered_sections.append({'name': name, 'items': section_items, 'image': None})

    return render(request, 'catering/menu.html', {'sections': ordered_sections})


# ---------------------------------------------------------------------------
# Admin dashboard: catering package / menu item / category management
# ---------------------------------------------------------------------------

@admin_required
def dashboard_home(request):
    return render(request, 'catering/dashboard/dashboard_home.html', {
        'package_count': CateringPackage.objects.count(),
        'category_count': Category.objects.count(),
        'menu_item_count': MenuItem.objects.count(),
    })


@admin_required
def package_manage_list(request):
    packages = CateringPackage.objects.select_related('category').all()
    return render(request, 'catering/dashboard/package_manage_list.html', {'packages': packages})


@admin_required
def package_create(request):
    if request.method == 'POST':
        form = CateringPackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catering package created.')
            return redirect('catering:package_manage_list')
    else:
        form = CateringPackageForm()
    return render(request, 'catering/dashboard/package_form.html', {'form': form, 'title': 'Add Catering Package'})


@admin_required
def package_update(request, pk):
    package = get_object_or_404(CateringPackage, pk=pk)
    if request.method == 'POST':
        form = CateringPackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catering package updated.')
            return redirect('catering:package_manage_list')
    else:
        form = CateringPackageForm(instance=package)
    return render(request, 'catering/dashboard/package_form.html', {'form': form, 'title': 'Edit Catering Package'})


@admin_required
def package_delete(request, pk):
    package = get_object_or_404(CateringPackage, pk=pk)
    if request.method == 'POST':
        package.delete()
        messages.success(request, 'Catering package deleted.')
        return redirect('catering:package_manage_list')
    return render(request, 'catering/dashboard/confirm_delete.html', {'object': package})


@admin_required
def menu_item_manage_list(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'catering/dashboard/menu_item_manage_list.html', {'menu_items': menu_items})


@admin_required
def menu_item_create(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item added.')
            return redirect('catering:menu_item_manage_list')
    else:
        form = MenuItemForm()
    return render(request, 'catering/dashboard/package_form.html', {'form': form, 'title': 'Add Menu Item'})


@admin_required
def menu_item_update(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated.')
            return redirect('catering:menu_item_manage_list')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'catering/dashboard/package_form.html', {'form': form, 'title': 'Edit Menu Item'})


@admin_required
def menu_item_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Menu item deleted.')
        return redirect('catering:menu_item_manage_list')
    return render(request, 'catering/dashboard/confirm_delete.html', {'object': item})


@admin_required
def category_manage_list(request):
    categories = Category.objects.all()
    return render(request, 'catering/dashboard/category_manage_list.html', {'categories': categories})


@admin_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added.')
            return redirect('catering:category_manage_list')
    else:
        form = CategoryForm()
    return render(request, 'catering/dashboard/package_form.html', {'form': form, 'title': 'Add Category'})


@admin_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated.')
            return redirect('catering:category_manage_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'catering/dashboard/package_form.html', {'form': form, 'title': 'Edit Category'})


@admin_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('catering:category_manage_list')
    return render(request, 'catering/dashboard/confirm_delete.html', {'object': category})
