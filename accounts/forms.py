from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)

from .models import CustomUser, CustomerProfile


def add_form_control(attrs=None):
    if attrs is None:
        attrs = {}
    existing = attrs.get('class', '')
    if 'form-control' not in existing:
        attrs['class'] = f'{existing} form-control'.strip()
    return attrs


class CustomerRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'phone', 'address', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = add_form_control(field.widget.attrs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'customer'
        if commit:
            user.save()
            CustomerProfile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone', ''),
                address=self.cleaned_data.get('address', ''),
            )
        return user


class DriverRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    license_number = forms.CharField(max_length=50)
    license_expiry = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = (
            'email', 'username', 'first_name', 'last_name',
            'phone', 'address', 'password1', 'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = add_form_control(field.widget.attrs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'driver'
        if commit:
            user.save()
            from drivers.models import DriverProfile
            DriverProfile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone', ''),
                address=self.cleaned_data.get('address', ''),
                license_number=self.cleaned_data['license_number'],
                license_expiry=self.cleaned_data['license_expiry'],
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autofocus': True}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = add_form_control(field.widget.attrs)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone', 'address')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = add_form_control(field.widget.attrs)


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ('phone', 'address', 'date_of_birth')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = add_form_control(field.widget.attrs)


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = add_form_control(field.widget.attrs)
