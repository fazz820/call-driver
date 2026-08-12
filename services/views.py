from django.shortcuts import get_object_or_404, render

from .models import Service


def service_detail(request, slug):
    service = get_object_or_404(Service.objects.select_related('category'), slug=slug, is_active=True)
    related_services = Service.objects.filter(
        category=service.category, is_active=True
    ).exclude(pk=service.pk)[:3]
    return render(request, 'core/service_detail.html', {
        'service': service,
        'related_services': related_services,
    })
