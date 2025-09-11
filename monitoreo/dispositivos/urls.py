from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("devices/", views.devices, name="devices"),
    path('devices/<int:device_id>/', views.device_detail, name='device_detail'),
    path("measurements/", views.measurements, name="measurements"),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('logout/', views.logout, name='logout'),
]

