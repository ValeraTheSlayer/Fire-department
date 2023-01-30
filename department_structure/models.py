from django.db import models
from city.models import City

# class City(models.Model):
#     name = models.CharField(max_length=30, unique=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         ordering = ["name"]
#         verbose_name_plural = "Города"
#         verbose_name = "Город"


class FireDepartment(models.Model):
    name = models.CharField(max_length=20, verbose_name='Пожарная часть')
    number_fighters = models.IntegerField(default=1, verbose_name='Кол-во бойцов')
    address_location = models.CharField(max_length=250, null=True, blank=True, verbose_name='Адрес ПЧ')
    year_of_construction = models.IntegerField(verbose_name='Год постройки', null=True, blank=True)
    year_of_renewal = models.IntegerField(verbose_name='Дата капитального ремонта', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Пожарные части"
        verbose_name = "Пожарная часть"

    def __str__(self):
        return str(self.name)
