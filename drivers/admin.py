import csv

from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.html import format_html

from .models import DriverProfile, Vehicle


class VehicleInline(admin.TabularInline):
    model = Vehicle
    extra = 0
    readonly_fields = ('created_at', 'updated_at')


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_preview', 'user', 'phone', 'license_number', 'is_available', 'rating', 'total_trips', 'created_at')
    list_filter = ('is_available', 'rating')
    list_select_related = ('user',)
    search_fields = ('user__email', 'user__username', 'license_number', 'phone')
    inlines = [VehicleInline]
    readonly_fields = ('created_at', 'updated_at', 'profile_preview_large')
    date_hierarchy = 'created_at'
    actions = ['mark_available', 'mark_unavailable', 'export_csv']

    def profile_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="35" height="35" style="object-fit:cover;border-radius:50%;">', obj.profile_image.url)
        return format_html('<i class="bi bi-person-circle" style="font-size:1.5rem;"></i>')
    profile_preview.short_description = ''

    def profile_preview_large(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="max-width:200px;max-height:200px;object-fit:cover;border-radius:8px;">', obj.profile_image.url)
        return 'No image uploaded'
    profile_preview_large.short_description = 'Profile Image Preview'

    def mark_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f'{updated} driver(s) marked as available.', messages.SUCCESS)
    mark_available.short_description = 'Mark selected as Available'

    def mark_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f'{updated} driver(s) marked as unavailable.', messages.SUCCESS)
    mark_unavailable.short_description = 'Mark selected as Unavailable'

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="drivers.csv"'
        writer = csv.writer(response)
        writer.writerow(['Email', 'Name', 'Phone', 'License', 'Available', 'Rating', 'Trips'])
        for d in queryset.select_related('user'):
            writer.writerow([
                d.user.email, d.user.get_full_name(), d.phone,
                d.license_number, d.is_available, d.rating, d.total_trips,
            ])
        return response
    export_csv.short_description = 'Export selected to CSV'


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'driver', 'make', 'model', 'year', 'license_plate', 'vehicle_type', 'is_active'
    )
    list_filter = ('vehicle_type', 'is_active', 'year')
    list_select_related = ('driver__user',)
    search_fields = ('license_plate', 'make', 'model', 'driver__user__email')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['export_csv']

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="vehicles.csv"'
        writer = csv.writer(response)
        writer.writerow(['Driver', 'Make', 'Model', 'Year', 'Plate', 'Type', 'Active'])
        for v in queryset.select_related('driver__user'):
            writer.writerow([v.driver.user.email, v.make, v.model, v.year, v.license_plate, v.vehicle_type, v.is_active])
        return response
    export_csv.short_description = 'Export selected to CSV'
