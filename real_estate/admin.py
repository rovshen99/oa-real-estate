from django.contrib import admin
from django.utils.html import format_html

from .models import City, RealEstate, RealEstateImage


class RealEstateImageInline(admin.TabularInline):
    model = RealEstateImage
    extra = 3
    fields = ('image', 'image_preview',)
    readonly_fields = ('image_preview',)

    def image_preview(self, instance):
        if instance.image:
            return format_html('<img src="{}" width="150" height="auto"/>', instance.image.url)
        return "No image uploaded."

    image_preview.short_description = 'Image Preview'


class RealEstateAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'price_display', 'city', 'is_available')
    list_filter = ('city', 'is_available')
    search_fields = ('title', 'address', 'description')
    readonly_fields = ('created_by', 'updated_by')
    inlines = [RealEstateImageInline]

    def price_display(self, obj):
        return format_html(f"{obj.price} {obj.currency}")


admin.site.register(City)
admin.site.register(RealEstate, RealEstateAdmin)