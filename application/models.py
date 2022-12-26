from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from department_structure.models import FireDepartment
from transport.models import Transport
from city.models import City
channel_layer = get_channel_layer()



# class City(models.Model):
#     name = models.CharField(max_length=30, unique=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         ordering = ["name"]
#         verbose_name_plural = "Города"
#         verbose_name = "Город"



class BorderPost(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Посты"
        verbose_name = "Пост"


class QuestionCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Категория вопросов"
        verbose_name = "Категория вопроса"

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    sip_number = models.CharField(max_length=9, unique=True, null=True, blank=True)
    operator = models.BooleanField(default=True, null=True, blank=True)
    department = models.ForeignKey(FireDepartment, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name='Пожарная часть (если не оператор)')
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Пользователи ПО"
        verbose_name = "Пользователя ПО"

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_info(sender, instance, **kwargs):
    instance.userinfo.save()


class StatisticCallNumber(models.Model):
    operator = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Оператор')
    date = models.DateField(null=True, blank=True, verbose_name='Дата')
    call_number = models.IntegerField(default=0, verbose_name='Кол-во принятых звонков')

    class Meta:
        verbose_name_plural = "Кол-во принятых звонков"
        verbose_name = "Кол-во принятых звонков"

    def __str__(self):
        if self.operator:
            text = ' Оператор ' + str(self.operator.sip_number) + ' на ' + str(self.date) + ' кол-во ' \
                   + str(self.call_number)
        else:
            text = ' Пограничная служба на ' + str(self.date) + ' кол-во ' + str(self.call_number)
        return text

    def save(self, *args, **kwargs):
        super(StatisticCallNumber, self).save(*args, **kwargs)
        # AFTER SAVING RECORD HERE WE SEND SOCKET MESSAGE TO FRONT END TO UPDATE DASHBOARD
        res = StatisticCallNumber.objects.filter(date=datetime.now().date())
        res_list = list()
        for rr in res:
            if rr.operator:
                res_list.append(['Оператор ' + str(rr.operator.sip_number), rr.call_number])
            else:
                res_list.append(['Переведено в ПС', rr.call_number])
        print(res_list)
        async_to_sync(channel_layer.group_send)('statistic',
                                                {'type': 'send_statics_call_number',
                                                 'operators': res_list,
                                                 })


class StatisticQuestionCategory(models.Model):
    question_category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE,
                                          verbose_name='Категория вопроса')
    date = models.DateField(null=True, blank=True, verbose_name='Дата')
    call_number = models.IntegerField(default=0, verbose_name='Кол-во принятых звонков')

    class Meta:
        verbose_name_plural = "Кол-во по категории вопросов"
        verbose_name = "Кол-во по категории вопросов"

    def __str__(self):
        return str(self.question_category.name) + ' на ' + str(self.date) + ' кол-во ' \
               + str(self.call_number)

    def save(self, *args, **kwargs):
        super(StatisticQuestionCategory, self).save(*args, **kwargs)
        # AFTER SAVING RECORD HERE WE SEND SOCKET MESSAGE TO FRONT END TO UPDATE DASHBOARD
        res = StatisticQuestionCategory.objects.filter(date=datetime.now().date())
        res_list = list()
        for rr in res:
            res_list.append([rr.question_category.name, rr.call_number])
        print(res_list)
        async_to_sync(channel_layer.group_send)('statistic',
                                                {'type': 'send_statics_question_category',
                                                 'question_category': res_list,
                                                 })

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

class CurrentAppeal(models.Model):
    user_created_event = models.ForeignKey(UserInfo, on_delete=models.CASCADE,
                                           verbose_name='Пользователь кто создал путевку')
    date_of_call_start = models.DateTimeField(blank=True, null=True, verbose_name='Время начала звонка')
    date_of_call_end = models.DateTimeField(blank=True, null=True, verbose_name='Время конца звонка')
    income_call_number = models.BigIntegerField(blank=True, null=True, verbose_name='Номер тел. клиента')
    callback_number = models.BigIntegerField(blank=True, null=True, verbose_name='Номер для обратной связи')
    income_call_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='ФИО заявителя')
    citizenship = models.CharField(max_length=100, blank=True, null=True, verbose_name='Гражданство')
    iin = models.CharField(max_length=12, blank=True, null=True, verbose_name='ИИН заявителя')
    borderpost = models.ForeignKey(BorderPost, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)


    #changing
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name='Адрес')
    emergency_type = models.ForeignKey(EmergencyType, on_delete=models.CASCADE, null=True, blank=True,
                                       verbose_name='Тип выезда')
    emergency_rank = models.ForeignKey(EmergencyRank, on_delete=models.CASCADE, null=True, blank=True,
                                       verbose_name='Ранг выезда')                                       
    object_owner = models.CharField(max_length=100, blank=True, null=True, verbose_name='Владелец объекта')
    emergency_closed = models.BooleanField(default=False, verbose_name='Вызов закрыть')
    object_category = models.ForeignKey(ObjectCategory, on_delete=models.CASCADE, null=True, blank=True, 
    verbose_name='Тип объекта')


    street = models.CharField(max_length=200, blank=True, null=True, verbose_name='Улица')
    house = models.CharField(max_length=5, blank=True, null=True, verbose_name='Дом')
    flat = models.CharField(max_length=3, blank=True, null=True, verbose_name='Кв')
    email = models.EmailField(blank=True, null=True)
    question_category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE,
                                          verbose_name='Категория вопроса')
    short_question = models.TextField(max_length=500, blank=True, null=True,
                                      verbose_name='Краткая фабула вопроса обращения')
    answer_to_short_question = models.TextField(max_length=500, blank=True, null=True,
                                                verbose_name='Ответ на вопрос обращения')

    ResponsibleDepartment = (
        ('c', 'CALL ЦЕНТР'),
        ('d', 'ПОГРАНИЧНАЯ СЛУЖБА'),
    )
    responsible_department = models.CharField(max_length=1, choices=ResponsibleDepartment, default='c')
    responsible_department_person = models.CharField(max_length=150, blank=True, null=True)
    

    status = models.BooleanField(default=True, verbose_name='Рассмотрен')
    api_unique_id = models.OneToOneField('ApiData', on_delete=models.CASCADE, null=True, blank=True)

    department = models.ManyToManyField(FireDepartment, verbose_name='Пожарная часть')
    transport = models.ManyToManyField(Transport, verbose_name='Привлеченные силы и средства', blank=True)

    class Meta:
        verbose_name_plural = "Текущие обращения"
        verbose_name = "Текущее обращение"

    def __str__(self):
        return ' Карта номер ' + str(self.id)

    def save(self, *args, **kwargs):
        super(CurrentAppeal, self).save(*args, **kwargs)
        # AFTER SAVING RECORD HERE STARTS CALCULATION OF STATISTICS

        # print(self.question_category)
        # print(self.user_created_event)
        # print(self.responsible_department)
        # print(self.status)
        # print(self.date_of_call_start.date())
        try:
            if self.status and self.responsible_department == 'c':
                obj = StatisticCallNumber.objects.get(operator=self.user_created_event,
                                                      date=self.date_of_call_start.date())
                call_number = len(CurrentAppeal.objects.filter(user_created_event=self.user_created_event,
                                                               date_of_call_start__year=
                                                               self.date_of_call_start.date().year,
                                                               date_of_call_start__month=
                                                               self.date_of_call_start.date().month,
                                                               date_of_call_start__day=
                                                               self.date_of_call_start.date().day,
                                                               status=True,
                                                               responsible_department='c'
                                                               ))
                # print('CALL NUMBER CALL CENTER OPERATORS', call_number)
                obj.call_number = call_number
                obj.save()
            elif self.status and self.responsible_department == 'd':
                obj = StatisticCallNumber.objects.get(operator__isnull=True,
                                                      date=self.date_of_call_start.date())
                call_number = len(CurrentAppeal.objects.filter(date_of_call_start__year=
                                                               self.date_of_call_start.date().year,
                                                               date_of_call_start__month=
                                                               self.date_of_call_start.date().month,
                                                               date_of_call_start__day=
                                                               self.date_of_call_start.date().day,
                                                               status=True,
                                                               responsible_department='d'
                                                               ))
                # print('CALL NUMBER DEPARTMENT BORDER SERVICE ', call_number)
                obj.call_number = call_number
                obj.save()
        except StatisticCallNumber.DoesNotExist:
            if self.status and self.responsible_department == 'c':
                obj = StatisticCallNumber(operator=self.user_created_event, date=self.date_of_call_start.date(),
                                          call_number=1)
                obj.save()
            elif self.status and self.responsible_department == 'd':
                obj = StatisticCallNumber(date=self.date_of_call_start.date(),
                                          call_number=1)
                obj.save()
        try:
            obj = StatisticQuestionCategory.objects.get(question_category=self.question_category,
                                                        date=self.date_of_call_start.date())
            call_number = len(CurrentAppeal.objects.filter(question_category=self.question_category,
                                                           date_of_call_start__year=
                                                           self.date_of_call_start.date().year,
                                                           date_of_call_start__month=
                                                           self.date_of_call_start.date().month,
                                                           date_of_call_start__day=
                                                           self.date_of_call_start.date().day,
                                                           status=True,
                                                           responsible_department='c'
                                                           ))
            # print('CALL NUMBER QUESTION CATEGORY', call_number)
            obj.call_number = call_number
            obj.save()
        except StatisticQuestionCategory.DoesNotExist:
            if self.status:
                obj = StatisticQuestionCategory(question_category=self.question_category,
                                                date=self.date_of_call_start.date(), call_number=1)
                obj.save()


class JournalEvent(models.Model):
    emergency = models.ForeignKey(CurrentAppeal, on_delete=models.CASCADE, verbose_name='Выезд - Текущие')
    event = models.CharField(max_length=500, blank=True, null=True, verbose_name='Событие')
    date_insert = models.DateTimeField(verbose_name='Время')

    class Meta:
        verbose_name_plural = "Журнал событий"
        verbose_name = "Событие"

    def __str__(self):
        return str(self.event) + ' - ' + str(self.date_insert)      


class DefaultEvent(models.Model):
    name = models.CharField(max_length=500, verbose_name='Cобытие')

    class Meta:
        verbose_name_plural = "Список частых событий (для журнала событий)"
        verbose_name = "Событие"

    def __str__(self):
        return self.name




class ApiData(models.Model):
    unique_id = models.CharField(max_length=20, unique=True)
    number_in = models.CharField(max_length=20, verbose_name='Номер тел. клиента')
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    first_api = models.BooleanField(default=False)
    second_api = models.BooleanField(default=False)
    downloaded = models.BooleanField(default=False)
    mark_quality = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.unique_id)


class KnowledgeBase(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=4000, blank=True)
    section = models.CharField(max_length=150, blank=True)
    reference_answer = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return 'Вопрос: {} - Ответ: {}'.format(self.question, self.answer)



  
