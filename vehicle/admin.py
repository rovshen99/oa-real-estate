from django.contrib import admin
from .models import Vehicle, Location, Brand, Name, GPSModel


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'brand', 'imei', 'number_sim', 'gps_model', 'installation_date', 'holder',
                    'fuse_5a', 'remarks', 'executor', 'location')
    search_fields = ('number', 'name__name', 'brand__name', 'imei', 'number_sim', 'gps_model__name')
    list_filter = ('gps_model', 'installation_date', 'brand', 'location')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Name)
class NameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(GPSModel)
class GPSModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
