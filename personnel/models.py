from django.db import models
from department_structure.models import FireDepartment


class Sentry(models.Model):
    name = models.CharField(max_length=80, unique=True, null=True, verbose_name='Название')

    class Meta:
        verbose_name_plural = "Караулы"
        verbose_name = "Караул"

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Должность')
    main_position = models.BooleanField(default=False, verbose_name='Должности которые только из ЦОУСС менять можно')
    fire_fighter = models.BooleanField(default=True, verbose_name='Те кто выезжает на пожар, боевые')


    class Meta:
        verbose_name_plural = "Должности"
        verbose_name = "Должность"

    def __str__(self):
        return self.name


class Status(models.Model):
    status = models.CharField(max_length=50, unique=True, null=True,
                              verbose_name='Примечание ЛС')

    class Meta:
        verbose_name_plural = "Примечания личного состава"
        verbose_name = "Примечание"

    def __str__(self):
        return self.status


class Staff(models.Model):
    unique_id = models.CharField(max_length=12, unique=True, verbose_name='ИИН')
    full_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ф.И.О.')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Должность')
    department = models.ForeignKey(FireDepartment, on_delete=models.CASCADE, verbose_name='ПЧ')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Примечание',
                               null=True, blank=True)

    gdzs = models.BooleanField(default=True, verbose_name='ГДЗС')
    sentry = models.ForeignKey(
        Sentry,
        on_delete=models.CASCADE,
        related_name='staffs',
        verbose_name='караул',
    )

    class Meta:
        verbose_name_plural = "Сотрудники"
        verbose_name = "Сотрудник"

    def __str__(self):
        return self.full_name
