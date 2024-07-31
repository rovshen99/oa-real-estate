from django.contrib import admin
from .models import (
    VehicleBrand, VehicleName, GPSTrackerModel, Location,
    VehicleCategory, Vehicle, SparePart, MaintenanceRecord,
    MaintenancePart, Supplier, SparePartOrder, SparePartOrderItem, FuelType, OilChangeRecord, VehicleCondition, FuelRecord
)


class VehicleBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class VehicleNameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class GPSTrackerModelAdmin(admin.ModelAdmin):
    list_display = ('model',)
    search_fields = ('model',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class VehicleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class MaintenancePartInline(admin.TabularInline):
    model = MaintenancePart
    extra = 1


class MaintenanceRecordInline(admin.TabularInline):
    model = MaintenanceRecord
    extra = 1
    inlines = [MaintenancePartInline]


class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'date', 'work_order_number', 'mechanic')
    search_fields = ('vehicle__registration_number', 'work_order_number', 'mechanic')
    inlines = [MaintenancePartInline]


class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'registration_number', 'brand', 'name', 'vin',
        'engine_number', 'gps_tracker', 'installation_date',
        'location', 'category', 'total_distance'
    )
    search_fields = ('registration_number', 'vin', 'engine_number')
    list_filter = ('brand', 'gps_tracker', 'location', 'category')
    inlines = [MaintenanceRecordInline]


class SparePartAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


class SparePartOrderItemInline(admin.TabularInline):
    model = SparePartOrderItem
    extra = 1


class SparePartOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'supplier', 'date', 'warehouse', 'total_cost')
    search_fields = ('order_number', 'supplier__name', 'warehouse')
    list_filter = ('supplier', 'date')
    inlines = [SparePartOrderItemInline]


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class FuelTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class OilChangeRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'date', 'mileage', 'next_oil_change_date', 'next_oil_change_mileage')
    search_fields = ('vehicle__registration_number', 'date')


class VehicleConditionAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'date', 'condition', 'reason')
    search_fields = ('vehicle__registration_number', 'date', 'condition')


class FuelRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'date', 'fuel_type', 'amount')
    search_fields = ('vehicle__registration_number', 'date', 'fuel_type__name')


admin.site.register(VehicleBrand, VehicleBrandAdmin)
admin.site.register(VehicleName, VehicleNameAdmin)
admin.site.register(GPSTrackerModel, GPSTrackerModelAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(VehicleCategory, VehicleCategoryAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(SparePart, SparePartAdmin)
admin.site.register(MaintenanceRecord, MaintenanceRecordAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(SparePartOrder, SparePartOrderAdmin)
admin.site.register(FuelType, FuelTypeAdmin)
admin.site.register(OilChangeRecord, OilChangeRecordAdmin)
admin.site.register(VehicleCondition, VehicleConditionAdmin)
admin.site.register(FuelRecord, FuelRecordAdmin)
