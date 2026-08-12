from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from accounts.mixins import AdminRequiredMixin, CustomerRequiredMixin, DriverOrAdminRequiredMixin

from .forms import AssignDriverForm, BookingCreateForm, BookingStatusUpdateForm
from .models import Booking, BookingStatus


class BookingCreateView(LoginRequiredMixin, CustomerRequiredMixin, CreateView):
    model = Booking
    form_class = BookingCreateForm
    template_name = 'bookings/booking_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Book a Ride'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.customer = self.request.user
        messages.success(self.request, 'Booking created successfully.')
        return super().form_valid(form)


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        qs = Booking.objects.select_related('customer', 'driver__user', 'service')
        if user.user_type == 'customer':
            return qs.filter(customer=user)
        if user.user_type == 'driver':
            return qs.filter(driver__user=user)
        return qs


class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'

    def get_object(self, queryset=None):
        qs = self.get_queryset().select_related(
            'customer', 'driver__user', 'service', 'payment'
        ).prefetch_related('status_logs')
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = get_object_or_404(qs, pk=pk)
        user = self.request.user
        if user.user_type == 'customer' and obj.customer != user:
            raise Http404
        if user.user_type == 'driver' and obj.driver and obj.driver.user != user:
            raise Http404
        return obj


class BookingStatusUpdateView(LoginRequiredMixin, DriverOrAdminRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingStatusUpdateForm
    template_name = 'bookings/booking_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update Status - Booking {self.object.id}'
        return context

    def form_valid(self, form):
        new_status = form.cleaned_data['status']
        self.object.log_status_change(new_status, form.cleaned_data.get('notes', ''), user=self.request.user)
        messages.success(self.request, f'Booking status updated to {dict(BookingStatus.choices)[new_status]}.')
        return super().form_valid(form)


class AssignDriverView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Booking
    form_class = AssignDriverForm
    template_name = 'bookings/booking_assign_driver.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Assign Driver - Booking {self.object.id}'
        return context

    def form_valid(self, form):
        booking = form.save()
        if booking.status == BookingStatus.PENDING:
            booking.status = BookingStatus.CONFIRMED
            booking.save(update_fields=['status'])
            booking.log_status_change(BookingStatus.CONFIRMED, 'Driver assigned', user=self.request.user)
        messages.success(self.request, f'Driver assigned to booking {booking.id}.')
        return super().form_valid(form)


class BookingCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk, customer=request.user)
        if not booking.can_cancel:
            messages.error(request, 'This booking cannot be cancelled.')
            return redirect('bookings:detail', pk=pk)
        booking.status = BookingStatus.CANCELLED
        booking.save(update_fields=['status'])
        booking.log_status_change(BookingStatus.CANCELLED, 'Cancelled by customer', user=request.user)
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('bookings:list')
