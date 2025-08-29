from django.contrib import admin

# Register your models here.
from .models import Categoria, Zona, Dispositivo, Medicion, Alerta

admin.site.register([Categoria, Zona, Dispositivo, Medicion, Alerta])
