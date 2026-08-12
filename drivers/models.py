from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def profile_image_path(instance, filename):
    return f'drivers/{instance.user.id}/profile/{filename}'


def license_image_path(instance, filename):
    return f'drivers/{instance.user.id}/license/{filename}'


class VehicleType(models.TextChoices):
    SEDAN = 'sedan', 'Sedan'
    SUV = 'suv', 'SUV'
    VAN = 'van', 'Van'
    LUXURY = 'luxury', 'Luxury'
    MINIBUS = 'minibus', 'Minibus'


class DriverProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='driver_profile',
        limit_choices_to={'user_type': 'driver'},
    )
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry = models.DateField()
    profile_image = models.ImageField(
        upload_to=profile_image_path, blank=True, null=True
    )
    license_image = models.ImageField(
        upload_to=license_image_path, blank=True, null=True,
        help_text='Upload a clear photo of your driving license',
    )
    is_available = models.BooleanField(default=True, db_index=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_trips = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-rating']),
            models.Index(fields=['is_available', '-rating']),
        ]

    def clean(self):
        if self.license_expiry and self.license_expiry < timezone.now().date():
            raise ValidationError({'license_expiry': 'License has already expired.'})

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.email} - {self.license_number}'


class Vehicle(models.Model):
    driver = models.ForeignKey(
        DriverProfile, on_delete=models.CASCADE, related_name='vehicles'
    )
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=30)
    license_plate = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(
        max_length=10, choices=VehicleType.choices, default=VehicleType.SEDAN
    )
    capacity = models.PositiveIntegerField(default=4)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['driver', 'is_active']),
        ]

    def clean(self):
        current_year = timezone.now().year
        if self.year < 1990 or self.year > current_year + 1:
            raise ValidationError({'year': f'Year must be between 1990 and {current_year + 1}.'})

    def __str__(self):
        return f'{self.make} {self.model} ({self.license_plate})'
