from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .auth_helpers import has_role


def role_required(*roles, login_url=None, redirect_url='dashboard:home'):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url=login_url)
        def wrapper(request, *args, **kwargs):
            if not has_role(request.user, *roles):
                role_names = ', '.join(r.capitalize() for r in roles)
                messages.error(
                    request,
                    f'Access denied. This area requires {role_names} privileges.',
                )
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def customer_required(function=None, **kwargs):
    if function:
        return role_required('customer')(function)
    return role_required('customer', **kwargs)


def driver_required(function=None, **kwargs):
    if function:
        return role_required('driver')(function)
    return role_required('driver', **kwargs)


def admin_required(function=None, **kwargs):
    if function:
        return role_required('admin')(function)
    return role_required('admin', **kwargs)


def driver_or_admin_required(function=None, **kwargs):
    if function:
        return role_required('driver', 'admin')(function)
    return role_required('driver', 'admin', **kwargs)
