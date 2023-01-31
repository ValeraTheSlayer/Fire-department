from django.db import models


class FireHydrant(models.Model):
    user_comments = models.TextField(max_length=100, verbose_name='Комментарии')
    latitude = models.DecimalField(max_digits=15, decimal_places=15, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=15, decimal_places=15, verbose_name='Долгота')
    raw_address = models.TextField(max_length=100, verbose_name='Адрес')
    working = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Гидранты города"
        verbose_name = "Гидрант"

    def __str__(self):
        return self.description