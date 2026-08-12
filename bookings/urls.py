from django.urls import path

from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.BookingListView.as_view(), name='list'),
    path('create/', views.BookingCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.BookingDetailView.as_view(), name='detail'),
    path('<uuid:pk>/status/', views.BookingStatusUpdateView.as_view(), name='status_update'),
    path('<uuid:pk>/assign/', views.AssignDriverView.as_view(), name='assign_driver'),
    path('<uuid:pk>/cancel/', views.BookingCancelView.as_view(), name='cancel'),
]
