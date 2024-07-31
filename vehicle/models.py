from django.db import models


class VehicleBrand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название бренда")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бренд транспортного средства"
        verbose_name_plural = "Бренды транспортных средств"


class VehicleName(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название транспортного средства")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Название транспортного средства"
        verbose_name_plural = "Названия транспортных средств"


class GPSTrackerModel(models.Model):
    model = models.CharField(max_length=100, verbose_name="Модель GPS трекера")

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "Модель GPS трекера"
        verbose_name_plural = "Модели GPS трекеров"


class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Локация")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class VehicleCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория транспортного средства")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория транспортного средства"
        verbose_name_plural = "Категории транспортных средств"


class Vehicle(models.Model):
    registration_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Регистрационный номер")
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Бренд")
    name = models.ForeignKey(VehicleName, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Название")
    vin = models.CharField(max_length=100, blank=True, null=True, verbose_name="VIN")
    engine_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Номер двигателя")
    gps_tracker = models.ForeignKey(GPSTrackerModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="GPS трекер")
    installation_date = models.DateField(null=True, blank=True, verbose_name="Дата установки")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Локация")
    category = models.ForeignKey(VehicleCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    total_distance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общий пробег", null=True, blank=True)

    def __str__(self):
        return self.registration_number

    class Meta:
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"


class SparePart(models.Model):
    code = models.CharField(max_length=100, blank=True, null=True, verbose_name="Код")
    name = models.CharField(max_length=100, verbose_name="Название запчасти")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Запчасть"
        verbose_name_plural = "Запчасти"


class MaintenanceRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_records', verbose_name="Транспортное средство")
    date = models.DateField(verbose_name="Дата")
    work_order_number = models.CharField(max_length=100, verbose_name="Номер заказа на работу")
    mechanic = models.CharField(max_length=100, verbose_name="Механик")

    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.work_order_number}"

    class Meta:
        verbose_name = "Запись о техническом обслуживании"
        verbose_name_plural = "Записи о техническом обслуживании"


class MaintenancePart(models.Model):
    maintenance_record = models.ForeignKey(MaintenanceRecord, on_delete=models.CASCADE, related_name='parts', verbose_name="Запись о техническом обслуживании")
    part = models.ForeignKey(SparePart, on_delete=models.CASCADE, verbose_name="Запчасть")
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    def __str__(self):
        return f"{self.maintenance_record.work_order_number} - {self.part.name}"

    class Meta:
        verbose_name = "Запчасть для техобслуживания"
        verbose_name_plural = "Запчасти для техобслуживания"


class Supplier(models.Model):
    name = models.CharField(max_length=100, verbose_name="Поставщик")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"


class SparePartOrder(models.Model):
    order_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Номер заказа")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="Поставщик")
    date = models.DateField(verbose_name="Дата")
    warehouse = models.CharField(max_length=100, verbose_name="Склад")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")

    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name = "Заказ запчастей"
        verbose_name_plural = "Заказы запчастей"


class SparePartOrderItem(models.Model):
    order = models.ForeignKey(SparePartOrder, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    part = models.ForeignKey(SparePart, on_delete=models.CASCADE, verbose_name="Запчасть")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f"{self.order.order_number} - {self.part.name}"

    class Meta:
        verbose_name = "Элемент заказа запчастей"
        verbose_name_plural = "Элементы заказов запчастей"


class FuelType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип топлива")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип топлива"
        verbose_name_plural = "Типы топлива"


class OilChangeRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='oil_change_records', verbose_name="Транспорт")
    date = models.DateField(verbose_name="Дата замены масла")
    mileage = models.PositiveIntegerField(verbose_name="Пробег на момент замены масла")
    next_oil_change_date = models.DateField(verbose_name="Дата следующей замены масла", null=True, blank=True)
    next_oil_change_mileage = models.PositiveIntegerField(verbose_name="Пробег для следующей замены масла", null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.date}"

    class Meta:
        verbose_name = "Запись замены масла"
        verbose_name_plural = "Записи замены масла"


class VehicleCondition(models.Model):
    WORKING = 'working'
    NOT_WORKING = 'not_working'

    CONDITION_CHOICES = [
        (WORKING, 'Работает'),
        (NOT_WORKING, 'Не работает')
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='conditions', verbose_name="Транспорт")
    date = models.DateField(verbose_name="Дата")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, verbose_name="Состояние")
    reason = models.TextField(verbose_name="Причина", null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.condition} - {self.date}"

    class Meta:
        verbose_name = "Состояние транспортного средства"
        verbose_name_plural = "Состояния транспортных средств"


class FuelRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fuel_records', verbose_name="Транспорт")
    date = models.DateField(verbose_name="Дата")
    fuel_type = models.ForeignKey(FuelType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Тип топлива")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество топлива")

    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.fuel_type.name} - {self.amount}"

    class Meta:
        verbose_name = "Запись заправки топлива"
        verbose_name_plural = "Записи заправки топлива"
