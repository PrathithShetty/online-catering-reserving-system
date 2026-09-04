from datetime import date

from django import forms

from .models import CartItem, Order, Review

FORM_CONTROL = 'form-control'


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ('event_date', 'guest_count', 'special_requests')
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': FORM_CONTROL}),
            'guest_count': forms.NumberInput(attrs={'class': FORM_CONTROL}),
            'special_requests': forms.Textarea(attrs={
                'class': FORM_CONTROL, 'rows': 3, 'placeholder': 'Any special requests (optional)',
            }),
        }

    def __init__(self, *args, package=None, **kwargs):
        self.package = package
        super().__init__(*args, **kwargs)

    def clean_event_date(self):
        event_date = self.cleaned_data['event_date']
        if event_date < date.today():
            raise forms.ValidationError('Event date cannot be in the past.')
        return event_date

    def clean_guest_count(self):
        guest_count = self.cleaned_data['guest_count']
        if self.package:
            if guest_count < self.package.min_guests:
                raise forms.ValidationError(f'This package requires at least {self.package.min_guests} guests.')
            if guest_count > self.package.max_guests:
                raise forms.ValidationError(f'This package supports at most {self.package.max_guests} guests.')
        return guest_count


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('delivery_address', 'contact_phone')
        widgets = {
            'delivery_address': forms.Textarea(attrs={'class': FORM_CONTROL, 'rows': 3}),
            'contact_phone': forms.TextInput(attrs={'class': FORM_CONTROL}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.Select(
                attrs={'class': 'form-select'},
                choices=[(i, f'{i} star{"s" if i > 1 else ""}') for i in range(1, 6)],
            ),
            'comment': forms.Textarea(attrs={'class': FORM_CONTROL, 'rows': 3}),
        }
