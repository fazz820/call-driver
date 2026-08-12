from django.urls import path

from . import views

app_name = 'drivers'

urlpatterns = [
    path('dashboard/', views.DriverDashboardView.as_view(), name='dashboard'),
    path('profile/', views.DriverProfileUpdateView.as_view(), name='profile'),
    path('availability/', views.DriverAvailabilityToggleView.as_view(), name='availability_toggle'),
    path('bookings/', views.DriverBookingListView.as_view(), name='bookings'),
    path('vehicles/create/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/edit/', views.VehicleUpdateView.as_view(), name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
]
