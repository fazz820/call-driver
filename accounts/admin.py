import csv

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.http import HttpResponse

from .models import CustomUser, CustomerProfile


class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'user_type', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_verified', 'is_active')
    list_select_related = True
    search_fields = ('email', 'username', 'phone')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('phone', 'address', 'user_type', 'is_verified')}),
    )
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CustomerProfileInline]
    date_hierarchy = 'date_joined'
    actions = ['mark_verified', 'mark_unverified', 'export_csv']

    def mark_verified(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} user(s) marked as verified.', messages.SUCCESS)
    mark_verified.short_description = 'Mark selected users as verified'

    def mark_unverified(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} user(s) marked as unverified.', messages.SUCCESS)
    mark_unverified.short_description = 'Mark selected users as unverified'

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        writer = csv.writer(response)
        writer.writerow(['Email', 'Username', 'Name', 'User Type', 'Verified', 'Active', 'Joined'])
        for u in queryset:
            writer.writerow([u.email, u.username, u.get_full_name(), u.user_type, u.is_verified, u.is_active, u.date_joined])
        return response
    export_csv.short_description = 'Export selected to CSV'


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'loyalty_points', 'created_at')
    list_select_related = ('user',)
    search_fields = ('user__email', 'user__username', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    actions = ['export_csv']

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customer_profiles.csv"'
        writer = csv.writer(response)
        writer.writerow(['Email', 'Name', 'Phone', 'Loyalty Points', 'Created'])
        for p in queryset.select_related('user'):
            writer.writerow([p.user.email, p.user.get_full_name(), p.phone, p.loyalty_points, p.created_at])
        return response
    export_csv.short_description = 'Export selected to CSV'
