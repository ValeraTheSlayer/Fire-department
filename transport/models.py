from django.db import models
from department_structure.models import FireDepartment
#from application.models import FireDepartment

class Brand(models.Model):
    brand = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Марки"
        verbose_name = "Марка"

    def __str__(self):
        return self.brand


class Model(models.Model):
    model = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Модели"
        verbose_name = "Модель"

    def __str__(self):
        return self.model


class TransType(models.Model):
    name = models.CharField(max_length=15, unique=True)

    class Meta:
        verbose_name_plural = "Типы"
        verbose_name = "Тип"

    def __str__(self):
        return self.name


class TransStatus(models.Model):
    status = models.CharField(max_length=50, unique=True, null=True,
                              verbose_name='Примечание техники')

    class Meta:
        verbose_name_plural = "Примечания техники"
        verbose_name = "Примечание техники"

    def __str__(self):
        return self.status


class Transport(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Марка')
    type = models.ForeignKey(TransType, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='Тип')
    trans_model = models.ForeignKey(Model, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name='Модель')
    bort_number = models.CharField(max_length=10, null=True, blank=True, verbose_name='Бортовой номер')
    year_of_trans = models.IntegerField(null=True, blank=True, verbose_name='Год выпуска')
    year_of_exploitation = models.IntegerField(null=True, blank=True, verbose_name='Срок эксплуатации')
    season_to = models.BooleanField(default=True, verbose_name='Сезонное ТО')
    new_number = models.CharField(max_length=9, null=True, blank=True, verbose_name='Регистр. номер')
    department = models.ForeignKey(FireDepartment, on_delete=models.CASCADE,
                                   verbose_name='Департамент')

    class Meta:
        verbose_name_plural = "Транспорты"
        verbose_name = "Транспорт"

    def __str__(self):
        return self.brand.brand + ' [' + self.department.name + ']'