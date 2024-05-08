from django.contrib import admin
from django.utils.html import format_html

from .models import City, RealEstate, RealEstateImage, Payment, Client


class RealEstateImageInline(admin.TabularInline):
    model = RealEstateImage
    extra = 0
    fields = ('image', 'image_preview',)
    readonly_fields = ('image_preview',)

    def image_preview(self, instance):
        if instance.image:
            print(instance.image.url)
            return format_html('<img src="{}" width="150" height="auto"/>', instance.image.url)
        return "Изображение не загружено."

    # class Media:
    #     js = ('js/preview_image.js',)

    image_preview.short_description = 'Предпросмотр изображения'


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = ['client', 'date', 'amount', 'description']


class RealEstateAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'price_display', 'remaining_payment_display', 'city', 'is_available')
    # list_filter = ('city', 'is_available')
    search_fields = ('title', 'address', 'description')
    readonly_fields = ('created_by', 'updated_by')
    inlines = [RealEstateImageInline, PaymentInline]

    @admin.display(description='Осталось оплатить')
    def remaining_payment_display(self, obj):
        return obj.remaining_payment

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('payments')
        return queryset

    class Media:
        js = ('js/admin_custom.js',)

    def price_display(self, obj):
        return format_html(f"{obj.total_cost} {obj.currency}")
    price_display.short_description = 'Цена'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['client', 'real_estate', 'date', 'amount', 'description']
    list_filter = ['client', 'real_estate', 'date']


admin.site.register(City)
admin.site.register(RealEstate, RealEstateAdmin)
