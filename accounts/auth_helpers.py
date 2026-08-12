from django.conf import settings
from django.shortcuts import redirect


def has_role(user, *roles):
    if not user.is_authenticated:
        return False
    return user.user_type in roles


def is_customer(user):
    return has_role(user, 'customer')


def is_driver(user):
    return has_role(user, 'driver')


def is_admin(user):
    return user.is_authenticated and (has_role(user, 'admin') or user.is_superuser)


def get_role_name(user):
    if not user.is_authenticated:
        return None
    return user.user_type


def redirect_for_role(user):
    if not user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    if is_admin(user):
        return redirect('dashboard:admin_dashboard')
    if is_driver(user):
        return redirect('drivers:dashboard')
    return redirect('bookings:list')


def redirect_if_authenticated(user, fallback_url='dashboard:home'):
    if user.is_authenticated:
        return redirect(fallback_url)
    return None
