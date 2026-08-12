from django import forms

from drivers.models import DriverProfile

from .models import Booking, BookingStatus


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = (
            'service', 'pickup_location', 'dropoff_location',
            'pickup_time', 'notes',
        )
        widgets = {
            'pickup_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            if 'form-control' not in css:
                field.widget.attrs['class'] = f'{css} form-control'.strip()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.base_price = instance.service.base_price
        if instance.distance_km and instance.service.price_per_km:
            instance.distance_price = instance.distance_km * instance.service.price_per_km
        instance.total_price = instance.base_price + instance.distance_price
        if commit:
            instance.save()
            instance.log_status_change(BookingStatus.PENDING, 'Booking created', user=self.user)
        return instance


class AssignDriverForm(forms.ModelForm):
    driver = forms.ModelChoiceField(
        queryset=DriverProfile.objects.filter(is_available=True),
        required=True,
        label='Select Driver',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Booking
        fields = ('driver',)


class BookingStatusUpdateForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=BookingStatus.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        label='Status notes',
    )

    class Meta:
        model = Booking
        fields = ('status',)
