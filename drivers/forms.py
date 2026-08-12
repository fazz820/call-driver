from django import forms

from .models import DriverProfile, Vehicle


class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = (
            'phone', 'address', 'bio',
            'profile_image', 'license_image',
            'license_number', 'license_expiry',
        )
        widgets = {
            'license_expiry': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            if 'form-control' not in css and not isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = f'{css} form-control'.strip()
        self.fields['profile_image'].widget.attrs['class'] = 'form-control'
        self.fields['license_image'].widget.attrs['class'] = 'form-control'


class DriverAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = ('is_available',)


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = (
            'make', 'model', 'year', 'color',
            'license_plate', 'vehicle_type', 'capacity', 'is_active',
        )
        widgets = {
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            if 'form-control' not in css and 'form-select' not in css:
                field.widget.attrs['class'] = f'{css} form-control'.strip()
