import csv

from django.contrib import admin, messages
from django.http import HttpResponse

from .models import Booking, BookingStatus, BookingStatusLog, Payment


class BookingStatusLogInline(admin.TabularInline):
    model = BookingStatusLog
    extra = 0
    readonly_fields = ('created_at', 'created_by')
    can_delete = False


class PaymentInline(admin.StackedInline):
    model = Payment
    can_delete = False
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id_short', 'customer_email', 'driver_name', 'service', 'pickup_time', 'status', 'total_price'
    )
    list_filter = ('status', 'pickup_time', 'created_at')
    list_select_related = ('customer', 'driver__user', 'service')
    search_fields = ('customer__email', 'customer__username', 'pickup_location', 'dropoff_location')
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [BookingStatusLogInline, PaymentInline]
    date_hierarchy = 'created_at'
    actions = ['mark_confirmed', 'mark_completed', 'mark_cancelled', 'export_csv']

    def id_short(self, obj):
        return str(obj.id)[:8] + '...'
    id_short.short_description = 'ID'
    id_short.admin_order_field = 'id'

    def customer_email(self, obj):
        return obj.customer.email
    customer_email.short_description = 'Customer'
    customer_email.admin_order_field = 'customer__email'

    def driver_name(self, obj):
        return obj.driver.user.get_full_name() or obj.driver.user.email if obj.driver else '-'
    driver_name.short_description = 'Driver'
    driver_name.admin_order_field = 'driver__user__email'

    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status=BookingStatus.CONFIRMED)
        self.message_user(request, f'{updated} booking(s) confirmed.', messages.SUCCESS)
    mark_confirmed.short_description = 'Mark selected as Confirmed'

    def mark_completed(self, request, queryset):
        updated = queryset.update(status=BookingStatus.COMPLETED)
        self.message_user(request, f'{updated} booking(s) completed.', messages.SUCCESS)
    mark_completed.short_description = 'Mark selected as Completed'

    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status=BookingStatus.CANCELLED)
        self.message_user(request, f'{updated} booking(s) cancelled.', messages.SUCCESS)
    mark_cancelled.short_description = 'Mark selected as Cancelled'

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="bookings.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Customer', 'Driver', 'Service', 'Pickup', 'Dropoff', 'Pickup Time', 'Status', 'Total'])
        for b in queryset.select_related('customer', 'driver__user', 'service'):
            writer.writerow([
                b.id, b.customer.email, b.driver.user.email if b.driver else '',
                b.service.name, b.pickup_location, b.dropoff_location,
                b.pickup_time, b.status, b.total_price,
            ])
        return response
    export_csv.short_description = 'Export selected to CSV'


@admin.register(BookingStatusLog)
class BookingStatusLogAdmin(admin.ModelAdmin):
    list_display = ('booking_id_short', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('booking__id', 'created_by__email')
    date_hierarchy = 'created_at'

    def booking_id_short(self, obj):
        return str(obj.booking.id)[:8] + '...'
    booking_id_short.short_description = 'Booking'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'booking_id_short', 'amount', 'payment_method', 'status', 'transaction_id', 'paid_at'
    )
    list_filter = ('status', 'payment_method', 'paid_at')
    search_fields = ('transaction_id', 'booking__id', 'booking__customer__email')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'paid_at'
    actions = ['mark_completed', 'mark_refunded', 'export_csv']

    def booking_id_short(self, obj):
        return str(obj.booking.id)[:8] + '...'
    booking_id_short.short_description = 'Booking'

    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} payment(s) marked as completed.', messages.SUCCESS)
    mark_completed.short_description = 'Mark selected as Completed'

    def mark_refunded(self, request, queryset):
        updated = queryset.update(status='refunded')
        self.message_user(request, f'{updated} payment(s) marked as refunded.', messages.SUCCESS)
    mark_refunded.short_description = 'Mark selected as Refunded'

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="payments.csv"'
        writer = csv.writer(response)
        writer.writerow(['Booking ID', 'Amount', 'Method', 'Status', 'Transaction ID', 'Paid At'])
        for p in queryset.select_related('booking'):
            writer.writerow([p.booking.id, p.amount, p.payment_method, p.status, p.transaction_id, p.paid_at])
        return response
    export_csv.short_description = 'Export selected to CSV'
