from django.db import models


class Hydrants(models.Model):
    created_date = models.DateTimeField(verbose_name="Дата и время добавления марки", default=None)
    user_comments = models.TextField(max_length=100, verbose_name='Комментарии', default='Комментарии')
    latitude = models.FloatField(verbose_name='Широта', default=None)
    longitude = models.FloatField(verbose_name='Долгота', default=None)
    raw_address = models.TextField(max_length=100, verbose_name='Адрес', default=None)
    working = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Гидранты города"
        verbose_name = "Гидрант"


class FireHistory(models.Model):
    event_date = models.DateTimeField(verbose_name="Дата и время проишествия", default=None)
    user_comments = models.TextField(max_length=100, verbose_name='Комментарии', default='Комментарии')
    latitude = models.FloatField(verbose_name='Широта', default=None)
    longitude = models.FloatField(verbose_name='Долгота', default=None)
    raw_address = models.TextField(max_length=100, verbose_name='Адрес', default=None)

    class Meta:
        verbose_name_plural = "История пожаров"
        verbose_name = "Пожар"


class SecurePlaces(models.Model):
    created_date = models.DateTimeField(verbose_name="Дата и время добавления марки", default=None)
    user_comments = models.TextField(max_length=100, verbose_name='Комментарии', default='Комментарии')
    latitude = models.FloatField(verbose_name='Широта', default=None)
    longitude = models.FloatField(verbose_name='Долгота', default=None)
    raw_address = models.TextField(max_length=100, verbose_name='Адрес', default=None)

    class Meta:
        verbose_name_plural = "Объекты Повышеной Безопасности"
        verbose_name = "ОПБ"


class Polygon_1_Coordinates(models.Model):
    latitude = models.FloatField(verbose_name='Широта', default=None)
    longitude = models.FloatField(verbose_name='Долгота', default=None)

    class Meta:
        verbose_name_plural = "Область вызова СПЧ-1"
        verbose_name = "крайняя кордината желтой области СПЧ-1"


class Polygon_2_Coordinates(models.Model):
    latitude = models.FloatField(verbose_name='Широта', default=None)
    longitude = models.FloatField(verbose_name='Долгота', default=None)

    class Meta:
        verbose_name_plural = "Область вызова СПЧ-2"
        verbose_name = "крайняя кордината желтой области СПЧ-2"


class Polygon_3_Coordinates(models.Model):
    latitude = models.FloatField(verbose_name='Широта', default=None)
    longitude = models.FloatField(verbose_name='Долгота', default=None)

    class Meta:
        verbose_name_plural = "Область вызова СПЧ-3"
        verbose_name = "крайняя кордината желтой области СПЧ-3"


class Polygon_4_Coordinates(models.Model):
    latitude = models.FloatField(verbose_name='Широта', default=None)
    longitude = models.FloatField(verbose_name='Долгота', default=None)

    class Meta:
        verbose_name_plural = "Область вызова СПЧ-4"
        verbose_name = "крайняя кордината желтой области СПЧ-4"


class Polygon_5_Coordinates(models.Model):
    latitude = models.FloatField(verbose_name='Широта', default=None)
    longitude = models.FloatField(verbose_name='Долгота', default=None)

    class Meta:
        verbose_name_plural = "Область вызова СПЧ-5"
        verbose_name = "крайняя кордината желтой области СПЧ-5"
