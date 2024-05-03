from django.contrib.auth.models import User
from django.db import models


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
    price = models.IntegerField(verbose_name="Цена")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD', verbose_name="Валюта")
    total_area = models.FloatField(verbose_name="Общая площадь m²")
    living_area = models.FloatField(null=True, blank=True, verbose_name="Жилая площадь m²")
    kitchen_area = models.FloatField(null=True, blank=True, verbose_name="Площадь кухни m²")
    rooms = models.IntegerField(verbose_name="Количество комнат")
    balconies = models.IntegerField(default=0, verbose_name="Количество балконов")
    number_of_floors = models.IntegerField(blank=True, null=True, verbose_name="Количество этажей")
    floor = models.IntegerField(blank=True, null=True, verbose_name="Этаж")
    description = models.TextField(verbose_name="Описание")
    year_built = models.IntegerField(verbose_name="Год постройки")
    is_available = models.BooleanField(default=True, verbose_name="Доступность")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="Время последнего обновления")
    created_by = models.ForeignKey(User, related_name='real_estate_creator', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Создал")
    updated_by = models.ForeignKey(User, related_name='real_estate_updater', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Обновил")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "недвижимость"
        verbose_name_plural = "недвижимости"


class RealEstateImage(models.Model):
    real_estate = models.ForeignKey(RealEstate, related_name='images', on_delete=models.CASCADE, verbose_name="Недвижимость")
    image = models.ImageField(upload_to='real_estate_images/%Y/%m/%d/', verbose_name="Изображение")

    class Meta:
        verbose_name = "изображение недвижимости"
        verbose_name_plural = "изображения недвижимости"
