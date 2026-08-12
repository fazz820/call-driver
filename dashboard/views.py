from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView

from accounts.auth_helpers import redirect_for_role
from accounts.mixins import AdminRequiredMixin
from accounts.models import CustomUser
from bookings.models import Booking, BookingStatus
from core.models import ContactMessage
from drivers.models import DriverProfile


@login_required
def home(request):
    return redirect_for_role(request.user)


class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)

        total_bookings = Booking.objects.count()
        total_customers = CustomUser.objects.filter(user_type='customer').count()
        total_drivers = CustomUser.objects.filter(user_type='driver').count()
        total_drivers_available = DriverProfile.objects.filter(is_available=True).count()

        revenue = Booking.objects.filter(
            status=BookingStatus.COMPLETED
        ).aggregate(total=Sum('total_price'))['total'] or 0

        status_counts = Booking.objects.values('status').annotate(count=Count('id'))
        status_map = {s['status']: s['count'] for s in status_counts}
        pending_bookings = status_map.get('pending', 0)
        active_bookings = status_map.get('confirmed', 0) + status_map.get('in_progress', 0)
        completed_bookings = status_map.get('completed', 0)
        cancelled_bookings = status_map.get('cancelled', 0)

        recent_bookings = Booking.objects.select_related(
            'customer', 'driver__user', 'service'
        ).order_by('-created_at')[:10]

        unread_messages = ContactMessage.objects.filter(is_read=False).count()

        daily_bookings_qs = (
            Booking.objects.filter(created_at__gte=thirty_days_ago)
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )
        daily_revenue_qs = (
            Booking.objects.filter(
                created_at__gte=thirty_days_ago,
                status=BookingStatus.COMPLETED,
            )
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(daily_revenue=Sum('total_price'))
            .order_by('date')
        )

        daily_bookings_map = {e['date']: e['count'] for e in daily_bookings_qs}
        daily_revenue_map = {e['date']: float(e['daily_revenue'] or 0) for e in daily_revenue_qs}

        days_labels = []
        daily_bookings_list = []
        daily_revenue_list = []
        for i in range(29, -1, -1):
            day = (now - timedelta(days=i)).date()
            days_labels.append(day.strftime('%b %d'))
            daily_bookings_list.append(daily_bookings_map.get(day, 0))
            daily_revenue_list.append(daily_revenue_map.get(day, 0.0))

        status_dict = {s['status']: s['count'] for s in status_counts}
        status_labels = []
        status_data = []
        status_colors = {
            'pending': '#ffc107',
            'confirmed': '#0dcaf0',
            'in_progress': '#0d6efd',
            'completed': '#198754',
            'cancelled': '#dc3545',
            'no_show': '#6c757d',
        }
        status_bg_colors = []
        for s in BookingStatus.choices:
            code = s[0]
            status_labels.append(s[1])
            status_data.append(status_dict.get(code, 0))
            status_bg_colors.append(status_colors.get(code, '#6c757d'))

        context.update({
            'total_bookings': total_bookings,
            'total_customers': total_customers,
            'total_drivers': total_drivers,
            'total_drivers_available': total_drivers_available,
            'revenue': revenue,
            'pending_bookings': pending_bookings,
            'active_bookings': active_bookings,
            'completed_bookings': completed_bookings,
            'cancelled_bookings': cancelled_bookings,
            'unread_messages': unread_messages,
            'recent_bookings': recent_bookings,
            'days_labels': days_labels,
            'daily_bookings': daily_bookings_list,
            'daily_revenue': daily_revenue_list,
            'status_labels': status_labels,
            'status_data': status_data,
            'status_bg_colors': status_bg_colors,
        })
        return context
