from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.html import format_html

from .models import Service, ServiceCategory


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'sort_order', 'service_count', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    list_display_links = ('image_preview', 'name')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="40" height="40" style="object-fit:cover;border-radius:4px;">', obj.image.url)
        return format_html('<i class="bi bi-grid" style="font-size:1.5rem;color:#666;"></i>')
    image_preview.short_description = 'Image'

    def service_count(self, obj):
        return obj.services.count()
    service_count.short_description = 'Services'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'category', 'base_price', 'price_per_km', 'duration_minutes', 'is_active')
    list_filter = ('category', 'is_active')
    list_select_related = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'category__name')
    readonly_fields = ('created_at', 'updated_at', 'image_preview_large')
    date_hierarchy = 'created_at'
    list_display_links = ('image_preview', 'name')
    fieldsets = (
        (None, {'fields': ('category', 'name', 'slug', 'description', 'image', 'image_preview_large', 'video')}),
        ('Pricing', {'fields': ('base_price', 'price_per_km', 'duration_minutes')}),
        ('Status', {'fields': ('is_active',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    actions = ['activate', 'deactivate', 'export_csv']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="40" height="40" style="object-fit:cover;border-radius:4px;">', obj.image.url)
        return format_html('<i class="bi bi-car-front" style="font-size:1.5rem;color:#666;"></i>')
    image_preview.short_description = 'Image'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:300px;max-height:200px;object-fit:cover;border-radius:8px;">', obj.image.url)
        return 'No image uploaded'
    image_preview_large.short_description = 'Image Preview'

    def activate(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} service(s) activated.', messages.SUCCESS)
    activate.short_description = 'Activate selected services'

    def deactivate(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} service(s) deactivated.', messages.SUCCESS)
    deactivate.short_description = 'Deactivate selected services'

    def export_csv(self, request, queryset):
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="services.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Category', 'Base Price', 'Price/km', 'Duration', 'Active'])
        for s in queryset.select_related('category'):
            writer.writerow([s.name, s.category.name, s.base_price, s.price_per_km, s.duration_minutes, s.is_active])
        return response
    export_csv.short_description = 'Export selected to CSV'
