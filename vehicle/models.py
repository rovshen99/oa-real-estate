from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Локация", unique=True)

    class Meta:
        verbose_name = "локация"
        verbose_name_plural = "локации"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Марка", unique=True)

    class Meta:
        verbose_name = "марка"
        verbose_name_plural = "марки"

    def __str__(self):
        return self.name


class Name(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование", unique=True)

    class Meta:
        verbose_name = "наименование"
        verbose_name_plural = "наименования"

    def __str__(self):
        return self.name


class GPSModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Модель GPS трекера", unique=True)

    class Meta:
        verbose_name = "модель GPS трекера"
        verbose_name_plural = "модели GPS трекеров"

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    number = models.CharField(max_length=10, verbose_name="Гос. номер")
    name = models.ForeignKey(Name, on_delete=models.SET_NULL, null=True, verbose_name="Наименование")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, verbose_name="Марка")
    imei = models.CharField(max_length=20, verbose_name="IMEI")
    number_sim = models.CharField(max_length=20, verbose_name="Номер SIM")
    gps_model = models.ForeignKey(GPSModel, on_delete=models.SET_NULL, null=True, verbose_name="Модель GPS трекера")
    installation_date = models.DateField(verbose_name="Дата установки")
    holder = models.CharField(max_length=100, verbose_name="Предохранитель держатель")
    fuse_5a = models.CharField(max_length=50, verbose_name="Предохранитель 5A")
    remarks = models.TextField(verbose_name="Примечание", blank=True, null=True)
    executor = models.CharField(max_length=100, verbose_name="Исполнитель")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, verbose_name="Локация")

    class Meta:
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"

    def __str__(self):
        return f"{self.number} - {self.name}"
