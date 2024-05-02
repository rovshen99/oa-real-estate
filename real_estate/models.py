from django.contrib.auth.models import User
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class RealEstate(models.Model):
    REAL_ESTATE_TYPES = (
        ('apartment', 'Квартира'),
        ('cottage', 'Коттедж'),
        ('house', 'Дом'),
    )
    CURRENCY_CHOICES = (
        ('USD', 'US Dollar'),
        ('TMT', 'Turkmenistan Manat'),
    )
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=20, choices=REAL_ESTATE_TYPES, default='apartment',
                            verbose_name='Тип недвижимости')
    price = models.IntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    total_area = models.FloatField()
    living_area = models.FloatField(null=True, blank=True)
    kitchen_area = models.FloatField(null=True, blank=True)
    rooms = models.IntegerField()
    balconies = models.IntegerField(default=0)
    number_of_floors = models.IntegerField(blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    year_built = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='real_estate_creator', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    updated_by = models.ForeignKey(User, related_name='real_estate_updater', on_delete=models.SET_NULL, null=True,
                                   blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if 'request' in kwargs:
            self.updated_by = kwargs['request'].user
            del kwargs['request']
        super().save(*args, **kwargs)


class RealEstateImage(models.Model):
    real_estate = models.ForeignKey(RealEstate, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='real_estate_images/%Y/%m/%d/')
