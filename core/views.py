from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, render

from drivers.models import DriverProfile
from services.models import Service, ServiceCategory

from .forms import ContactForm
from .models import SiteSettings, Testimonial


def _get_settings():
    return SiteSettings.objects.first()


def home(request):
    services = Service.objects.filter(is_active=True).select_related('category')[:6]
    testimonials = Testimonial.objects.filter(is_approved=True)[:6]
    settings = _get_settings()
    return render(request, 'core/home.html', {
        'services': services,
        'testimonials': testimonials,
        'settings': settings,
    })


def about(request):
    settings = _get_settings()
    return render(request, 'core/about.html', {
        'settings': settings,
    })


def services(request):
    categories = ServiceCategory.objects.filter(
        services__is_active=True
    ).prefetch_related(
        models.Prefetch('services', queryset=Service.objects.filter(is_active=True))
    ).distinct()
    return render(request, 'core/services.html', {
        'categories': categories,
    })


def drivers(request):
    driver_list = DriverProfile.objects.filter(
        is_available=True
    ).select_related('user').prefetch_related('vehicles')
    return render(request, 'core/drivers.html', {
        'drivers': driver_list,
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent successfully! We will get back to you soon.')
            return redirect('core:contact')
    else:
        form = ContactForm()
    settings = _get_settings()
    return render(request, 'core/contact.html', {
        'form': form,
        'settings': settings,
    })
