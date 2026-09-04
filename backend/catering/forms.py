from django import forms

from .models import Category, CateringPackage, MenuItem

FORM_CONTROL = 'form-control'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': FORM_CONTROL}),
            'description': forms.Textarea(attrs={'class': FORM_CONTROL, 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': FORM_CONTROL}),
        }


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ('name', 'section', 'description', 'food_type', 'is_veg', 'price', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': FORM_CONTROL}),
            'section': forms.TextInput(attrs={
                'class': FORM_CONTROL, 'placeholder': 'e.g. Dosa Varieties (groups the public Menu page)',
            }),
            'description': forms.Textarea(attrs={'class': FORM_CONTROL, 'rows': 3}),
            'food_type': forms.Select(attrs={'class': 'form-select'}),
            'is_veg': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'price': forms.NumberInput(attrs={'class': FORM_CONTROL, 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': FORM_CONTROL}),
        }


class CateringPackageForm(forms.ModelForm):
    class Meta:
        model = CateringPackage
        fields = (
            'category', 'name', 'description', 'image', 'price_per_plate',
            'min_guests', 'max_guests', 'menu_items', 'is_active',
        )
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': FORM_CONTROL}),
            'description': forms.Textarea(attrs={'class': FORM_CONTROL, 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': FORM_CONTROL}),
            'price_per_plate': forms.NumberInput(attrs={'class': FORM_CONTROL}),
            'min_guests': forms.NumberInput(attrs={'class': FORM_CONTROL}),
            'max_guests': forms.NumberInput(attrs={'class': FORM_CONTROL}),
            'menu_items': forms.CheckboxSelectMultiple,
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
