# Generated by Django 5.0.4 on 2024-05-02 12:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0003_realestate_currency'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'город', 'verbose_name_plural': 'города'},
        ),
        migrations.AlterModelOptions(
            name='realestate',
            options={'verbose_name': 'недвижимость', 'verbose_name_plural': 'недвижимости'},
        ),
        migrations.AlterModelOptions(
            name='realestateimage',
            options={'verbose_name': 'изображение недвижимости', 'verbose_name_plural': 'изображения недвижимости'},
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название города'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='balconies',
            field=models.IntegerField(default=0, verbose_name='Количество балконов'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='real_estate.city', verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='real_estate_creator', to=settings.AUTH_USER_MODEL, verbose_name='Создал'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='currency',
            field=models.CharField(choices=[('USD', 'Доллар США'), ('TMT', 'Туркменский манат')], default='USD', max_length=3, verbose_name='Валюта'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='floor',
            field=models.IntegerField(blank=True, null=True, verbose_name='Этаж'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='Доступность'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='kitchen_area',
            field=models.FloatField(blank=True, null=True, verbose_name='Площадь кухни'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='living_area',
            field=models.FloatField(blank=True, null=True, verbose_name='Жилая площадь'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='number_of_floors',
            field=models.IntegerField(blank=True, null=True, verbose_name='Количество этажей'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='price',
            field=models.IntegerField(verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='rooms',
            field=models.IntegerField(verbose_name='Количество комнат'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='total_area',
            field=models.FloatField(verbose_name='Общая площадь'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='real_estate_updater', to=settings.AUTH_USER_MODEL, verbose_name='Обновил'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='Время последнего обновления'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='year_built',
            field=models.IntegerField(verbose_name='Год постройки'),
        ),
        migrations.AlterField(
            model_name='realestateimage',
            name='image',
            field=models.ImageField(upload_to='real_estate_images/%Y/%m/%d/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='realestateimage',
            name='real_estate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='real_estate.realestate', verbose_name='Недвижимость'),
        ),
    ]