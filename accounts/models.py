from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from .managers import CustomUserManager


class UserType(models.TextChoices):
    CUSTOMER = 'customer', 'Customer'
    DRIVER = 'driver', 'Driver'
    ADMIN = 'admin', 'Admin'


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    user_type = models.CharField(
        max_length=10, choices=UserType.choices, default=UserType.CUSTOMER
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['user_type']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['-date_joined']),
        ]

    def __str__(self):
        return self.email


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='customer_profile',
        limit_choices_to={'user_type': 'customer'},
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    loyalty_points = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.user.user_type != 'customer':
            raise ValidationError({'user': 'Profile can only be created for customers.'})

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.email}'
