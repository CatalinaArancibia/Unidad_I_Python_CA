from django.contrib import admin
from .models import Organization, OrganizationUser, Category, Product, Device, Measurement, Alert, Product_Alert, Model, Brand, Zone  

class OrganizationUserInline(admin.TabularInline):
    model = OrganizationUser
    extra = 1

class OrganizationAdmin(admin.ModelAdmin):
    inlines = [OrganizationUserInline]

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationUser)
admin.site.register([Category, Product, Device, Measurement, Alert, Product_Alert, Model, Brand, Zone])
