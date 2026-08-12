import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone


class BookingStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'
    NO_SHOW = 'no_show', 'No Show'


class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'
    REFUNDED = 'refunded', 'Refunded'


class PaymentMethod(models.TextChoices):
    CASH = 'cash', 'Cash'
    CARD = 'card', 'Card'
    ONLINE = 'online', 'Online'
    MOBILE_MONEY = 'mobile_money', 'Mobile Money'


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'user_type': 'customer'},
    )
    driver = models.ForeignKey(
        'drivers.DriverProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings',
    )
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.PROTECT,
        related_name='bookings',
    )
    pickup_location = models.TextField()
    dropoff_location = models.TextField()
    pickup_lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    pickup_lng = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    dropoff_lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    dropoff_lng = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    pickup_time = models.DateTimeField()
    status = models.CharField(
        max_length=15, choices=BookingStatus.choices, default=BookingStatus.PENDING,
        db_index=True,
    )
    distance_km = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    distance_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['pickup_time']),
            models.Index(fields=['created_at']),
            models.Index(fields=['customer', 'created_at']),
            models.Index(fields=['driver', 'created_at']),
        ]

    def __str__(self):
        return f'Booking {self.id} - {self.customer.email}'

    def get_absolute_url(self):
        return reverse('bookings:detail', kwargs={'pk': self.pk})

    def clean(self):
        if self.pickup_location and self.dropoff_location and self.pickup_location == self.dropoff_location:
            raise ValidationError('Pickup and dropoff locations must be different.')
        if self.pickup_time and self.pickup_time < timezone.now():
            raise ValidationError({'pickup_time': 'Pickup time must be in the future.'})

    def save(self, *args, **kwargs):
        if self.pk is None and not self.total_price:
            self.base_price = self.service.base_price
            if self.distance_km and self.service.price_per_km:
                self.distance_price = self.distance_km * self.service.price_per_km
            self.total_price = self.base_price + self.distance_price
        super().save(*args, **kwargs)

    @property
    def can_cancel(self):
        return self.status in (BookingStatus.PENDING, BookingStatus.CONFIRMED)

    @property
    def status_badge(self):
        badges = {
            BookingStatus.PENDING: 'warning',
            BookingStatus.CONFIRMED: 'info',
            BookingStatus.IN_PROGRESS: 'primary',
            BookingStatus.COMPLETED: 'success',
            BookingStatus.CANCELLED: 'danger',
            BookingStatus.NO_SHOW: 'secondary',
        }
        return badges.get(self.status, 'secondary')

    def log_status_change(self, status, notes='', user=None):
        BookingStatusLog.objects.create(
            booking=self,
            status=status,
            notes=notes,
            created_by=user,
        )


class BookingStatusLog(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name='status_logs'
    )
    status = models.CharField(max_length=15, choices=BookingStatus.choices)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='status_updates',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Booking status logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['booking', 'created_at']),
        ]

    def __str__(self):
        return f'{self.booking.id} -> {self.status}'


class Payment(models.Model):
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=15, choices=PaymentMethod.choices, default=PaymentMethod.CASH
    )
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    status = models.CharField(
        max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING,
        db_index=True,
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['booking', 'status']),
        ]

    def __str__(self):
        return f'Payment {self.transaction_id or self.id} - {self.booking.id}'
