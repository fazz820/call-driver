from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

from .auth_helpers import has_role


class RoleRequiredMixin(UserPassesTestMixin):
    roles = []
    permission_denied_message = 'Access denied.'
    permission_denied_url = 'dashboard:home'

    def test_func(self):
        return has_role(self.request.user, *self.roles)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.permission_denied_url)


class CustomerRequiredMixin(RoleRequiredMixin):
    roles = ['customer']
    permission_denied_message = 'Access denied. This area is for customers only.'


class DriverRequiredMixin(RoleRequiredMixin):
    roles = ['driver']
    permission_denied_message = 'Access denied. This area is for drivers only.'


class AdminRequiredMixin(RoleRequiredMixin):
    roles = ['admin']
    permission_denied_message = 'Access denied. This area is for administrators only.'


class DriverOrAdminRequiredMixin(RoleRequiredMixin):
    roles = ['driver', 'admin']
    permission_denied_message = 'Access denied. Only drivers and admins can access this area.'
