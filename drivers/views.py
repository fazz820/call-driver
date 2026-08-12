from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView, View

from accounts.mixins import DriverRequiredMixin
from bookings.models import Booking

from .forms import DriverAvailabilityForm, DriverProfileForm, VehicleForm
from .models import DriverProfile, Vehicle


class DriverDashboardView(LoginRequiredMixin, DriverRequiredMixin, TemplateView):
    template_name = 'drivers/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(DriverProfile, user=self.request.user)
        bookings = Booking.objects.filter(driver=profile)
        total = bookings.count()
        active = bookings.filter(status__in=('confirmed', 'in_progress')).count()
        completed = bookings.filter(status='completed').count()
        recent = bookings.select_related('customer', 'service').order_by('-created_at')[:5]
        vehicles = profile.vehicles.filter(is_active=True)
        context.update({
            'profile': profile,
            'total_bookings': total,
            'active_bookings': active,
            'completed_bookings': completed,
            'recent_bookings': recent,
            'vehicles': vehicles,
        })
        return context


class DriverProfileUpdateView(LoginRequiredMixin, DriverRequiredMixin, UpdateView):
    model = DriverProfile
    form_class = DriverProfileForm
    template_name = 'drivers/profile_form.html'
    success_url = reverse_lazy('drivers:dashboard')

    def get_object(self, queryset=None):
        return get_object_or_404(DriverProfile, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)


class DriverAvailabilityToggleView(LoginRequiredMixin, DriverRequiredMixin, View):
    def post(self, request):
        profile = get_object_or_404(DriverProfile, user=request.user)
        profile.is_available = not profile.is_available
        profile.save(update_fields=['is_available'])
        status = 'available' if profile.is_available else 'unavailable'
        messages.success(request, f'You are now marked as {status}.')
        return redirect('drivers:dashboard')


class DriverBookingListView(LoginRequiredMixin, DriverRequiredMixin, ListView):
    model = Booking
    template_name = 'drivers/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        profile = get_object_or_404(DriverProfile, user=self.request.user)
        return Booking.objects.filter(driver=profile).select_related(
            'customer', 'service'
        )


class VehicleCreateView(LoginRequiredMixin, DriverRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'drivers/vehicle_form.html'
    success_url = reverse_lazy('drivers:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Vehicle'
        return context

    def form_valid(self, form):
        profile = get_object_or_404(DriverProfile, user=self.request.user)
        form.instance.driver = profile
        messages.success(self.request, 'Vehicle added successfully.')
        return super().form_valid(form)


class VehicleUpdateView(LoginRequiredMixin, DriverRequiredMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'drivers/vehicle_form.html'
    success_url = reverse_lazy('drivers:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Vehicle'
        return context

    def get_queryset(self):
        profile = get_object_or_404(DriverProfile, user=self.request.user)
        return Vehicle.objects.filter(driver=profile)

    def form_valid(self, form):
        messages.success(self.request, 'Vehicle updated successfully.')
        return super().form_valid(form)


class VehicleDeleteView(LoginRequiredMixin, DriverRequiredMixin, DeleteView):
    model = Vehicle
    template_name = 'drivers/vehicle_confirm_delete.html'
    success_url = reverse_lazy('drivers:dashboard')

    def get_queryset(self):
        profile = get_object_or_404(DriverProfile, user=self.request.user)
        return Vehicle.objects.filter(driver=profile)

    def form_valid(self, form):
        messages.success(self.request, 'Vehicle removed successfully.')
        return super().form_valid(form)
