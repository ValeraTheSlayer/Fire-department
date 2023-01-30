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
    department = models.ForeignKey(FireDepartment, on_delete=models.CASCADE,
                                   verbose_name='Департамент', null=True)

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

    class Meta:
        verbose_name_plural = "Строевые записки по техникам"
        verbose_name = "Строевая записка"

    def __str__(self):
        return str(self.date_line_note)