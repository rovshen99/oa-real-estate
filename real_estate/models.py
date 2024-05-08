from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название города")

    class Meta:
        verbose_name = "город"
        verbose_name_plural = "города"

    def __str__(self):
        return self.name


class RealEstate(models.Model):
    REAL_ESTATE_TYPES = (
        ('apartment', 'Квартира'),
        ('cottage', 'Коттедж'),
        ('house', 'Дом'),
    )
    CURRENCY_CHOICES = (
        ('USD', 'Доллар США'),
        ('TMT', 'Туркменский манат'),
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name="Город")
    type = models.CharField(max_length=20, choices=REAL_ESTATE_TYPES, default='apartment', verbose_name="Тип недвижимости")
    total_cost = models.IntegerField(verbose_name="Цена недвижимости", default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD', verbose_name="Валюта")
    total_area = models.FloatField(verbose_name="Общая площадь m²")
    living_area = models.FloatField(null=True, blank=True, verbose_name="Жилая площадь m²")
    kitchen_area = models.FloatField(null=True, blank=True, verbose_name="Площадь кухни m²")
    rooms = models.IntegerField(verbose_name="Количество комнат")
    balconies = models.IntegerField(default=0, verbose_name="Количество балконов")
    number_of_floors = models.IntegerField(blank=True, null=True, verbose_name="Количество этажей", default=0)
    floor = models.IntegerField(blank=True, null=True, verbose_name="Этаж", default=0)
    description = models.TextField(verbose_name="Описание")
    year_built = models.IntegerField(verbose_name="Год постройки", default=datetime.now().year)
    is_available = models.BooleanField(default=True, verbose_name="Доступность")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="Время последнего обновления")
    created_by = models.ForeignKey(User, related_name='real_estate_creator', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Создал")
    updated_by = models.ForeignKey(User, related_name='real_estate_updater', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Обновил")

    def __str__(self):
        return self.title

    def remaining_payment(self):
        print(1)
        paid_total = sum(payment.amount for payment in self.payments.all())
        print(paid_total)
        return self.total_cost - paid_total

    class Meta:
        verbose_name = "недвижимость"
        verbose_name_plural = "недвижимости"


class Client(models.Model):
    name = models.CharField("Имя", max_length=255)
    email = models.EmailField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "покупатель"
        verbose_name_plural = "покупатели"

    def __str__(self):
        return self.name


class Payment(models.Model):
    client = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.CASCADE, related_name='payments')
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE, related_name='payments')
    date = models.DateField("Дата оплаты", default=timezone.now)
    amount = models.DecimalField("Сумма оплаты", max_digits=10, decimal_places=2)
    description = models.TextField("Описание", blank=True, null=True)

    class Meta:
        verbose_name = "оплата"
        verbose_name_plural = "оплаты"

    def __str__(self):
        return f"{self.client.name} paid {self.amount} on {self.date.strftime('%Y-%m-%d')}"


class RealEstateImage(models.Model):
    real_estate = models.ForeignKey(RealEstate, related_name='images', on_delete=models.CASCADE, verbose_name="Недвижимость")
    image = models.ImageField(upload_to='real_estate_images/%Y/%m/%d/', verbose_name="Изображение")

    class Meta:
        verbose_name = "изображение недвижимости"
        verbose_name_plural = "изображения недвижимости"
