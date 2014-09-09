from django.contrib import admin
from . import models


class CarrierAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'is_default']


class InsuranceAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'cost']


class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['order', 'carrier']


admin.site.register(models.Carrier, CarrierAdmin)
admin.site.register(models.Shipment, ShipmentAdmin)
admin.site.register(models.Insurance, InsuranceAdmin)
