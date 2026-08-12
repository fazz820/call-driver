import os

from django.db import models


def service_image_path(instance, filename):
    if instance.id:
        base, ext = os.path.splitext(filename)
        return f'services/{instance.slug}/{base}_{instance.id}{ext}'
    return f'services/{instance.slug}/{filename}'


def service_video_path(instance, filename):
    if instance.id:
        base, ext = os.path.splitext(filename)
        return f'services/{instance.slug}/videos/{base}_{instance.id}{ext}'
    return f'services/{instance.slug}/videos/{filename}'


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Bootstrap icon class')
    image = models.ImageField(upload_to='service_categories/', blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Service categories'
        ordering = ['sort_order']

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.CASCADE, related_name='services'
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=service_image_path, blank=True, null=True)
    video = models.FileField(upload_to=service_video_path, blank=True, null=True, help_text='Upload a background video for this service')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_km = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    duration_minutes = models.PositiveIntegerField(
        default=0, help_text='Estimated duration in minutes'
    )
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['category', 'is_active']),
        ]

    def __str__(self):
        return self.name
