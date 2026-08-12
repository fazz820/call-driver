from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from drivers.models import DriverProfile

from .forms import (
    CustomerProfileForm,
    CustomerRegistrationForm,
    CustomPasswordChangeForm,
    DriverRegistrationForm,
    LoginForm,
    ProfileUpdateForm,
)
from .models import CustomerProfile


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. Welcome!')
            return redirect('dashboard:home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/register_customer.html', {'form': form})


def register_driver(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Driver account created successfully. Welcome!')
            return redirect('dashboard:home')
    else:
        form = DriverRegistrationForm()
    return render(request, 'accounts/register_driver.html', {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().email}!')
        return super().form_valid(form)


@login_required
def profile(request):
    user = request.user
    profile = None
    profile_form = None

    if user.user_type == 'customer':
        profile, _ = CustomerProfile.objects.get_or_create(user=user)
        profile_form = CustomerProfileForm(instance=profile)
    elif user.user_type == 'driver':
        profile, _ = DriverProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=user)
        if user.user_type == 'customer':
            profile_form = CustomerProfileForm(request.POST, instance=profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('accounts:profile')
        else:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('accounts:profile')
    else:
        user_form = ProfileUpdateForm(instance=user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully.')
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)
