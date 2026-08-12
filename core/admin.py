import csv

from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.html import format_html

from .models import ContactMessage, SiteSettings, Testimonial


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'contact_phone')
    readonly_fields = ('created_at', 'updated_at', 'logo_preview', 'favicon_preview')
    fieldsets = (
        ('Branding', {'fields': ('site_name', 'tagline', 'logo', 'logo_preview', 'favicon', 'favicon_preview')}),
        ('Contact', {'fields': ('contact_email', 'contact_phone', 'address')}),
        ('Social', {'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url')}),
        ('Content', {'fields': ('about_text', 'working_hours', 'booking_terms', 'cancellation_policy')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height:60px;border-radius:4px;">', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo Preview'

    def favicon_preview(self, obj):
        if obj.favicon:
            return format_html('<img src="{}" style="max-height:32px;border-radius:2px;">', obj.favicon.url)
        return '-'
    favicon_preview.short_description = 'Favicon Preview'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    actions = ['mark_read', 'mark_unread', 'export_csv']

    def mark_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.', messages.SUCCESS)
    mark_read.short_description = 'Mark selected as Read'

    def mark_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.', messages.SUCCESS)
    mark_unread.short_description = 'Mark selected as Unread'

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="messages.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Subject', 'Message', 'Read', 'Date'])
        for m in queryset:
            writer.writerow([m.name, m.email, m.subject, m.message, m.is_read, m.created_at])
        return response
    export_csv.short_description = 'Export selected to CSV'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'content_preview', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating')
    search_fields = ('name', 'content')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    actions = ['approve', 'disapprove', 'export_csv']

    def content_preview(self, obj):
        return obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
    content_preview.short_description = 'Content'

    def approve(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} testimonial(s) approved.', messages.SUCCESS)
    approve.short_description = 'Approve selected testimonials'

    def disapprove(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} testimonial(s) disapproved.', messages.SUCCESS)
    disapprove.short_description = 'Disapprove selected testimonials'

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="testimonials.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Rating', 'Content', 'Approved', 'Date'])
        for t in queryset:
            writer.writerow([t.name, t.rating, t.content, t.is_approved, t.created_at])
        return response
    export_csv.short_description = 'Export selected to CSV'
