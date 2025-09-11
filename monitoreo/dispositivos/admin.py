from django.contrib import admin

# Register your models here.
from .models import Organization, Category, Product, Device, Measurement, Alert, Product_Alert, Model, Brand, Zone, User  

admin.site.register([Organization, Category, Product, Device, Measurement, Alert, Product_Alert, Model, Brand, Zone, User])
