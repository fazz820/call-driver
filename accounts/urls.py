from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/driver/', views.register_driver, name='register_driver'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
]
