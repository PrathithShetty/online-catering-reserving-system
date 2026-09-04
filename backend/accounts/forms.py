from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User

FORM_CONTROL = {'class': 'form-control'}


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(FORM_CONTROL)
        self.fields['password'].widget.attrs.update(FORM_CONTROL)


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs=FORM_CONTROL))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs=FORM_CONTROL))
    address = forms.CharField(widget=forms.Textarea(attrs={**FORM_CONTROL, 'rows': 2}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'address', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(FORM_CONTROL)
        self.fields['password1'].widget.attrs.update(FORM_CONTROL)
        self.fields['password2'].widget.attrs.update(FORM_CONTROL)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CUSTOMER
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '')
        user.address = self.cleaned_data.get('address', '')
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'address')
        widgets = {
            'first_name': forms.TextInput(attrs=FORM_CONTROL),
            'last_name': forms.TextInput(attrs=FORM_CONTROL),
            'email': forms.EmailInput(attrs=FORM_CONTROL),
            'phone': forms.TextInput(attrs=FORM_CONTROL),
            'address': forms.Textarea(attrs={**FORM_CONTROL, 'rows': 3}),
        }
