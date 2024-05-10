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
    house_number = models.IntegerField(verbose_name="Номер дома", blank=True, null=True,)
    building_number = models.IntegerField(verbose_name="Номер корпуса", blank=True, null=True)
    apartment_number = models.IntegerField(verbose_name="Номер квартиры", blank=True, null=True,)
    rooms_count = models.IntegerField(verbose_name="Количество комнат")
    floors_count = models.IntegerField(blank=True, null=True, verbose_name="Количество этажей", default=0)
    floor = models.IntegerField(blank=True, null=True, verbose_name="Этаж", default=0)
    description = models.TextField(verbose_name="Описание")
    year_built = models.IntegerField(verbose_name="Год постройки", default=datetime.now().year)
    is_available = models.BooleanField(default=True, verbose_name="Доступность")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="Время последнего обновления")
    created_by = models.ForeignKey(User, related_name='real_estate_creator', on_delete=models.SET_NULL, null=True,
                                   blank=True, verbose_name="Создал")
    updated_by = models.ForeignKey(User, related_name='real_estate_updater', on_delete=models.SET_NULL, null=True,
                                   blank=True, verbose_name="Обновил")

    def save(self, *args, **kwargs):
        if 'user' in kwargs:
            self.updated_by = kwargs.pop('user')
        self.updated_time = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def remaining_payment(self):
        payments = self.payments.all()
        if payments.count() > 0:
            paid_total = sum(payment.amount for payment in self.payments.all())
            return self.total_cost - paid_total
        return self.total_cost

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
    PAYMENT_CHOICES = (
        ("T", "Перечисление"),
        ("C", "Наличная оплата")
    )
    client = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.CASCADE, related_name='payments')
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE, related_name='payments')
    date = models.DateField(verbose_name="Дата оплаты", default=timezone.now)
    amount = models.DecimalField(verbose_name="Сумма оплаты", max_digits=10, decimal_places=2)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    receipt_number = models.CharField(verbose_name="Номер квитанции", max_length=100, blank=True, null=True)
    payment_type = models.CharField(verbose_name="Форма оплаты", max_length=1, choices=PAYMENT_CHOICES, default="C")

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
