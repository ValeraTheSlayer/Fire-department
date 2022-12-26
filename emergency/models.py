from django.db import models
from application.models import CurrentAppeal
# from users.models import User
from department_structure.models import FireDepartment
from transport.models import Transport
from personnel.models import Staff
from application.models import CurrentAppeal

class ObjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Категории объекта"
        verbose_name = "Категория объекта"

    def __str__(self):
        return self.name


class EmergencyRank(models.Model):
    rank = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name_plural = "Ранги"
        verbose_name = "Ранг"

    def __str__(self):
        return self.rank


class EmergencyType(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name_plural = "Типы"
        verbose_name = "Тип"

    def __str__(self):
        return self.name


# class CurrentEmergency(models.Model):
#     user_created_event = models.ForeignKey(User, on_delete=models.CASCADE,
#                                            verbose_name='Пользователь кто создал путевку')
#     date_of_call_start = models.DateTimeField(blank=True, null=True, verbose_name='Время начала звонка')
#     date_of_call_end = models.DateTimeField(blank=True, null=True, verbose_name='Время конца звонка')
#     income_call_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер тел. заявителя')
#     income_call_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='ФИО заявителя')
#     address = models.CharField(max_length=500, blank=True, null=True, verbose_name='Адрес')
#     object_category = models.ForeignKey(ObjectCategory, on_delete=models.CASCADE, null=True, blank=True,
#                                       verbose_name='Категория объекта')
#     object_owner = models.CharField(max_length=100, blank=True, null=True, verbose_name='Владелец объекта')
#     emergency_type = models.ForeignKey(EmergencyType, on_delete=models.CASCADE, null=True, blank=True,
#                                        verbose_name='Тип выезда')
#     emergency_rank = models.ForeignKey(EmergencyRank, on_delete=models.CASCADE, null=True, blank=True,
#                                        verbose_name='Ранг выезда')
#     emergency_closed = models.BooleanField(default=False, verbose_name='Вызов закрыть')
#     department = models.ManyToManyField(FireDepartment, verbose_name='Пожарная часть')

#     first_info_burning = models.CharField(max_length=1000, blank=True, null=True,
#                                           verbose_name='Первичная информация по сообщению')
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name='Руководитель тушение пожара')
#     transport = models.ManyToManyField(Transport, verbose_name='Привлеченные силы и средства', blank=True)

#     class Meta:
#         verbose_name_plural = "Поступившие заявки"
#         verbose_name = "Заявка"

#     def __str__(self):
#         return str(self.date_of_call_start) + ' | ' + str(self.address) + ' | ' + str(self.id)


class DefaultEvent(models.Model):
    name = models.CharField(max_length=500, verbose_name='Cобытие')

    class Meta:
        verbose_name_plural = "Список частых событий (для журнала событий)"
        verbose_name = "Событие"

    def __str__(self):
        return self.name


class JournalEvent(models.Model):
    emergency = models.ForeignKey(CurrentAppeal, on_delete=models.CASCADE, verbose_name='Выезд - Текущие')
    event = models.CharField(max_length=500, blank=True, null=True, verbose_name='Событие')
    date_insert = models.DateTimeField(verbose_name='Время')

    class Meta:
        verbose_name_plural = "Журнал событий"
        verbose_name = "Событие"

    def __str__(self):
        return str(self.event) + ' - ' + str(self.date_insert)