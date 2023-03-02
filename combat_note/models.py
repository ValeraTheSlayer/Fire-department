from django.db import models
from personnel.models import Position, Staff, Status
from department_structure.models import FireDepartment
from transport.models import Transport, TransStatus


class LineNoteMan(models.Model):
    date_line_note = models.DateField(verbose_name='Дата')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Должность')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, blank=True, null=True, verbose_name='ФИО')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Примечание', null=True, blank=True)
    gdzs = models.BooleanField(default=True, verbose_name='ГДЗС')
    department = models.ForeignKey(FireDepartment, on_delete=models.CASCADE, verbose_name='Департамент', null=True)
    class Meta:
        verbose_name_plural = "Строевые записки личного состава"
        verbose_name = "Строевая записка"

    def __str__(self):
        return str(self.date_line_note)


class LineNoteTrans(models.Model):
    date_line_note = models.DateField(verbose_name='Дата')
    department = models.ForeignKey(FireDepartment, on_delete=models.CASCADE,
                                   verbose_name='Департамент')
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, verbose_name='Транспорт')
    trans_status = models.ForeignKey(TransStatus, on_delete=models.CASCADE, verbose_name='Примечание техники',
                                     null=True, blank=True)
    gsm = models.IntegerField(default=0, verbose_name='ГСМ')
    foam = models.IntegerField(default=0, verbose_name='Пена')

    sleeves_77 = models.IntegerField(default=0, verbose_name='Рукава 77мм')
    sleeves_66 = models.IntegerField(default=0, verbose_name='Рукава 66мм')
    sleeves_51 = models.IntegerField(default=0, verbose_name='Рукава 51мм')

    fire_monitors_stationary = models.IntegerField(default=0, verbose_name='Лафетные сволы стационарные')
    fire_monitors_portable = models.IntegerField(default=0, verbose_name='Лафетные сволы переносные')

    gps_600 = models.IntegerField(default=0, verbose_name='ГПС - 600')
    blizzard = models.IntegerField(default=0, verbose_name='Пурга')
    portable_radios = models.IntegerField(default=0, verbose_name='переносные радиостанции')
    flashlight = models.IntegerField(default=0, verbose_name='электрофонарь')
    spotlight = models.IntegerField(default=0, verbose_name='прожектор')
    current = models.IntegerField(default=0, verbose_name='ТОК')
    l1 = models.IntegerField(default=0, verbose_name='Л - 1')
    rescue_ropes = models.IntegerField(default=0, verbose_name='спасательные веревки')

    class Meta:
        verbose_name_plural = "Строевые записки по техникам"
        verbose_name = "Строевая записка-техника "

    def __str__(self):
        return str(self.date_line_note)


class StaticValues(models.Model):
    date_additional_information = models.DateField(verbose_name='Дата')
    department = models.ForeignKey(FireDepartment, on_delete=models.CASCADE, verbose_name='Департамент')

    foam_stock = models.IntegerField(default=0, verbose_name='Пена на складе')
    hydra_costume = models.IntegerField(default=0, verbose_name='Гидрокостюм')
    motor_pumps_on_repair = models.IntegerField(default=0, verbose_name='мотопомпы на ремонте')
    motor_pumps_in_combat = models.IntegerField(default=0, verbose_name='мотопомпы в боевом расчете')
    class Meta:
        verbose_name_plural = "Дополнительная информация по строевой записке"
        verbose_name = "Информация"
    def __str__(self):
        return str(self.date_additional_information)