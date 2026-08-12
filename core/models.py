from django.conf import settings
from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='Call Driver Agency')
    tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True)
    favicon = models.ImageField(upload_to='logos/', blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    about_text = models.TextField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    working_hours = models.CharField(max_length=200, blank=True)
    booking_terms = models.TextField(blank=True)
    cancellation_policy = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Site settings'

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return self.site_name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_read', 'created_at']),
        ]

    def __str__(self):
        return f'{self.name} - {self.subject}'


class Testimonial(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='testimonials',
    )
    name = models.CharField(max_length=100, help_text='Display name')
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(
        default=5, help_text='Rating from 1 to 5'
    )
    is_approved = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_approved', '-created_at']),
        ]

    def __str__(self):
        return f'Testimonial by {self.name}'
