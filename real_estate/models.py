from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название города", unique=True)

    class Meta:
        verbose_name = "город"
        verbose_name_plural = "города"

    def __str__(self):
        return self.name


class RealEstateType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип недвижимости", unique=True)

    class Meta:
        verbose_name = "тип недвижимостей"
        verbose_name_plural = "типы недвижимостей"

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")

    class Meta:
        verbose_name = "объект"
        verbose_name_plural = "объекты"

    def __str__(self):
        return self.title


class RealEstate(models.Model):
    CURRENCY_CHOICES = (
        ('USD', 'Доллар США'),
        ('TMT', 'Туркменский манат'),
    )
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='real_estates', verbose_name="Объект",
                                blank=True, null=True)
    house_number = models.CharField(max_length=10, verbose_name="Номер дома", blank=True, null=True,)
    entrance_number = models.IntegerField(verbose_name="Номер подъезда", blank=True, null=True,)
    apartment_number = models.IntegerField(verbose_name="Номер квартиры (офиса, магазина)", blank=True, null=True,)
    building = models.CharField(max_length=10, verbose_name="Корпус", blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name="Город")
    type = models.ForeignKey(RealEstateType, on_delete=models.SET_NULL, null=True, verbose_name="Тип недвижимости")
    cost_per_sqm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                       verbose_name='Фактическая стоимость за квадратный метр')
    total_cost = models.DecimalField(verbose_name="Фактическая стоимость недвижимости", blank=True, null=True,
                                     max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD', verbose_name="Валюта")
    total_area = models.FloatField(verbose_name="Общая площадь m²")
    rooms_count = models.IntegerField(verbose_name="Количество комнат")
    floor = models.IntegerField(blank=True, null=True, verbose_name="Этаж", default=0)
    floors_count = models.IntegerField(verbose_name="Количество этажей", default=0)
    description = models.TextField(verbose_name="Примечание", blank=True, null=True)
    year_built = models.IntegerField(verbose_name="Год постройки", default=datetime.now().year)
    is_available = models.BooleanField(default=True, verbose_name="Доступность")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="Время последнего обновления")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='real_estate_creator', on_delete=models.SET_NULL, null=True,
                                   blank=True, verbose_name="Создал")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='real_estate_updater', on_delete=models.SET_NULL, null=True,
                                   blank=True, verbose_name="Обновил")

    def save(self, *args, **kwargs):
        if 'user' in kwargs:
            self.updated_by = kwargs.pop('user')
        self.updated_time = timezone.now()
        super().save(*args, **kwargs)

    def clean(self):
        if self.total_cost and self.total_cost < 0:
            raise ValidationError("Цена не может быть ниже нуля.")

    def __str__(self):
        if self.project:
            return self.project.title
        return ""

    class Meta:
        verbose_name = "недвижимость"
        verbose_name_plural = "недвижимости"


class Buyer(models.Model):
    name = models.CharField("Имя", max_length=255)
    email = models.EmailField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "покупатель"
        verbose_name_plural = "покупатели"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    real_estate = models.ForeignKey(RealEstate, verbose_name="Недвижимость", on_delete=models.CASCADE, related_name='transactions')
    buyer = models.ForeignKey(Buyer, verbose_name="Покупатель", on_delete=models.SET_NULL, null=True, related_name='purchases')
    date = models.DateField(verbose_name="Дата сделки", null=True, blank=True)
    amount = models.DecimalField(verbose_name="Сумма сделки",max_digits=12, decimal_places=2)
    is_completed = models.BooleanField(default=False, verbose_name='Сделка завершена')

    def __str__(self):
        status = "Сделка завершена" if self.is_completed else "Сделка еще не завершена"
        return f"{self.date} - {self.real_estate} ({status})"

    def remaining_payment(self):
        payments = self.payments.all()
        if payments.count() > 0:
            paid_total = sum(payment.amount for payment in self.payments.all())
            return self.amount - paid_total
        return self.amount

    def clean(self):
        if self.amount and self.amount < 0:
            raise ValidationError("Цена не может быть ниже нуля.")

    class Meta:
        verbose_name = "сделка"
        verbose_name_plural = "сделки"


# class Payment(models.Model):
#     PAYMENT_CHOICES = (
#         ("T", "Перечисление"),
#         ("C", "Наличная оплата")
#     )
#     buyer = models.ForeignKey(Buyer, verbose_name="Клиент", on_delete=models.CASCADE, related_name='payments')
#     real_estate = models.ForeignKey(RealEstate, verbose_name="Недвижимостъ", on_delete=models.CASCADE, related_name='payments')
#     date = models.DateField(verbose_name="Дата оплаты", default=timezone.now)
#     amount = models.DecimalField(verbose_name="Сумма оплаты", max_digits=10, decimal_places=2)
#     description = models.TextField(verbose_name="Примечание", blank=True, null=True)
#     receipt_number = models.CharField(verbose_name="Номер квитанции", max_length=100, blank=True, null=True)
#     payment_type = models.CharField(verbose_name="Форма оплаты", max_length=1, choices=PAYMENT_CHOICES, default="C")
#
#     class Meta:
#         verbose_name = "оплата"
#         verbose_name_plural = "оплаты"
#
#     def __str__(self):
#         return f"{self.buyer.name} paid {self.amount} on {self.date.strftime('%Y-%m-%d')}"

class Payment(models.Model):
    PAYMENT_CHOICES = (
        ("T", "Перечисление"),
        ("C", "Наличная оплата"),
        ("M", "Взаиморассчет")
    )
    transaction = models.ForeignKey(Transaction, verbose_name="Сделка", on_delete=models.CASCADE,
                                    related_name='payments', blank=True, null=True)
    amount = models.DecimalField(verbose_name="Сумма оплаты", max_digits=10, decimal_places=2)
    receipt_number = models.CharField(verbose_name="Номер квитанции", max_length=100, blank=True, null=True)
    payment_type = models.CharField(verbose_name="Форма оплаты", max_length=1, choices=PAYMENT_CHOICES, default="C")
    description = models.TextField(verbose_name="Примечание", blank=True, null=True)
    date = models.DateField(verbose_name="Дата оплаты", default=timezone.now)

    class Meta:
        verbose_name = "оплата"
        verbose_name_plural = "оплаты"

    def __str__(self):
        return f"{self.date} - {self.amount} оплачено для {self.transaction}"


class RealEstateImage(models.Model):
    real_estate = models.ForeignKey(RealEstate, related_name='images', on_delete=models.CASCADE, verbose_name="Недвижимость")
    image = models.ImageField(upload_to='real_estate_images/%Y/%m/%d/', verbose_name="Изображение")

    class Meta:
        verbose_name = "изображение недвижимости"
        verbose_name_plural = "изображения недвижимости"
