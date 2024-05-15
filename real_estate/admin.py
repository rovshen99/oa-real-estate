from django.contrib import admin
from django.utils.html import format_html

from .models import City, RealEstate, RealEstateImage, Payment, Buyer, RealEstateType, Transaction


class RealEstateImageInline(admin.StackedInline):
    model = RealEstateImage
    extra = 0
    fields = ('image', 'image_preview',)
    readonly_fields = ('image_preview',)

    def image_preview(self, instance):
        if instance.image:
            print(instance.image.url)
            return format_html('<img src="{}" width="150" height="auto"/>', instance.image.url)
        return "Изображение не загружено."

    image_preview.short_description = 'Предпросмотр изображения'


class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    fields = ['amount', 'description', "payment_type", "receipt_number", 'date', ]


class TransactionInline(admin.StackedInline):
    model = Transaction
    extra = 0
    fields = ['buyer', 'date', 'amount', 'is_completed']
    raw_id_fields = ['buyer']
    inlines = [PaymentInline]


# @admin.register(RealEstate)
# class RealEstateAdmin(admin.ModelAdmin):
#     list_display = ('title', 'address', 'price_display', 'remaining_payment_display', 'city', 'is_available')
#     search_fields = ('title', 'address', 'description')
#     readonly_fields = ('created_by', 'updated_by', 'remaining_payment_display')
#     inlines = [RealEstateImageInline, PaymentInline]
#
#     def save_model(self, request, obj, form, change):
#         obj.save(user=request.user)
#         super().save_model(request, obj, form, change)
#
#     @admin.display(description='Осталось оплатить')
#     def remaining_payment_display(self, obj):
#         return obj.remaining_payment()
#
#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         queryset = queryset.prefetch_related('payments')
#         return queryset
#
#     def price_display(self, obj):
#         return format_html(f"{obj.total_cost} {obj.currency}")
#     price_display.short_description = 'Цена'

@admin.register(RealEstate)
class RealEstateAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'type', 'is_available', 'total_cost')
    list_filter = ('city', 'is_available', 'type')
    search_fields = ('title', 'description', 'address')
    inlines = [RealEstateImageInline]
    readonly_fields = ('created_time', 'created_by', 'updated_time', 'updated_by')
    fieldsets = (
        (None, {
            'fields': (
                'title', 'address', 'house_number', 'building', 'apartment_number', 'city', 'type', 'total_area',
                'rooms_count', 'floor', 'description', 'year_built', 'is_available', 'cost_per_sqm', 'total_cost',
                'currency')
        }),
        ('Дополнительные данные', {
            'classes': ('collapse',),
            'fields': ('created_time', 'created_by', 'updated_time', 'updated_by'),
        }),
    )

    # def save_model(self, request, obj, form, change):
    #     obj.save(user=request.user)
    #     super().save_model(request, obj, form, change)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['real_estate', 'buyer', 'date', 'amount', 'is_completed']
    list_filter = ['is_completed', 'date', 'buyer', 'real_estate']
    search_fields = ['real_estate__title', 'buyer__name']
    inlines = [PaymentInline]


@admin.register(RealEstateType)
class RealEstateTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
