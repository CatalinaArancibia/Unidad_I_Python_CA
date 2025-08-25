from django.urls import path
from . import views

urlpatterns = [
    path("panel1/", views.panel_dispositivos, name="panel_dispositivos"),
]

