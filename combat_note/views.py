import os
from django.http import FileResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters import rest_framework as dj_filter
from .serializers import LineNoteManSerializer, LineNoteTransSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .filters import LineNoteManFilter, LineNoteTransFilter
from .models import LineNoteMan, LineNoteTrans
from .services.reports import create_report_line_note
from department_structure.models import FireDepartment
from personnel.models import Position, Status
from transport.models import TransStatus
from django.conf import settings


class LineNoteManViewSet(viewsets.ModelViewSet):
    """Вьюшки по строевым запискам по сотрудникам."""
    queryset = LineNoteMan.objects.all()
    serializer_class = LineNoteManSerializer
    filter_backends = [dj_filter.DjangoFilterBackend, ]
    filter_class = LineNoteManFilter


class LineNoteTransViewSet(viewsets.ModelViewSet):
    """Вьюшки по строевым запискам по транспортам."""
    queryset = LineNoteTrans.objects.all()
    serializer_class = LineNoteTransSerializer
    filter_backends = [dj_filter.DjangoFilterBackend, ]
    filter_class = LineNoteTransFilter


@swagger_auto_schema(
    methods=['GET', ],
    operation_description='Получение отчета по строевым запискам',
    manual_parameters=[
        openapi.Parameter(
            'date_insert',
            in_=openapi.IN_PATH,
            description='Дата отчета',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: "ok",
    }
)
@api_view(['GET'])
def line_note_report(request, date_insert):
    # LINE NOTE OF STAFF
    line_note_staff_base = LineNoteMan.objects.filter(date_line_note=date_insert, position__main_position=False,
                                                      staff__department__city=request.user.city)
    # LINE NOTE OF TRANSPORT
    line_note_transport = LineNoteTrans.objects.filter(date_line_note=date_insert,
                                                       department__city=request.user.city)
    departments = FireDepartment.objects.filter(city=request.user.city).order_by('name')

    report = list()
    # Для 3 Налицо личного состава (Начальники караулов)
    head_list = [pos.id for pos in Position.objects.filter(name__startswith='Начальник')]
    # Для 4 Налицо личного состава (Командиры отделений)
    commander_list = [pos.id for pos in Position.objects.filter(name__startswith='Командир')]
    # Для 5 Налицо личного состава (Водители)
    driver = Position.objects.get(name='Водитель')
    # Для 6 Налицо личного состава (Пожарный)
    fire_fighter = Position.objects.get(name='Пожарный')
    # Для 7 Налицо личного состава (Диспетчеров (радиотелефонистов))
    call_assistant = Position.objects.get(name='Диспетчер')
    # Для 9 Отсутствуют (Отпуск учебный/декрет.)
    vacation = Status.objects.get(status='Отпуск')
    # Для 10 Отсутствуют (Больные)
    sick = Status.objects.get(status='Больничный')
    # Для 11 Отсутствуют (Командировка)
    business_trip = Status.objects.get(status='Командировка')
    # Для 12 Отсутствуют (Другие причины)
    others = Status.objects.get(status='Другие причины')
    # Для 15 Пожарная техника (В резерве(Тип основного пожарного автомобиля))
    # Для 16 Пожарная техника (В резерве(Марка специального.пожарного автомобиля))
    reserve_status = TransStatus.objects.get(status='В резерве')
    # Для 17 Пожарная техника (На ремонте(Тип основного пожарного автомобиля))
    # Для 18 Пожарная техника (На ремонте(Марка специального.пожарного автомобиля))
    renovation_status = TransStatus.objects.get(status='На ремонте')
    for dep in departments:
        # 13 Пожарная техника (В расчете(Тип основного пожарного автомобиля))
        counting_brand = [line.transport.brand.brand for line in line_note_transport.filter(department=dep,
                                                                                            trans_status__status="В расчете")]
        # 14 Пожарная техника (В расчете(Марка специального.пожарного автомобиля))
        counting_model = [line.transport.trans_model.model for line in
                          line_note_transport.filter(department=dep, trans_status__status="В расчете")]
        # 15 Пожарная техника (В резерве(Тип основного пожарного автомобиля))
        reserve_brand = [line.transport.brand.brand for line in line_note_transport.filter(department=dep,
                                                                                           trans_status=reserve_status)]
        # 16 Пожарная техника (В резерве(Марка специального.пожарного автомобиля))
        reserve_model = [line.transport.trans_model.model for line in line_note_transport.filter(department=dep,
                                                                                                 trans_status=
                                                                                                 reserve_status)]
        # 17 Пожарная техника (На ремонте(Тип основного пожарного автомобиля))
        renovation_brand = [line.transport.brand.brand for line in line_note_transport.filter(department=dep,
                                                                                              trans_status=
                                                                                              renovation_status)]
        # 18 Пожарная техника (На ремонте(Марка специального.пожарного автомобиля))
        renovation_model = [line.transport.trans_model.model for line in
                            line_note_transport.filter(department=dep, trans_status=renovation_status)]
        # print('MAXIMUM IS ', max([len(counting_brand), len(reserve_model), len(renovation_model)]))
        # print("RENOVATION is ", counting_brand, counting_model)
        # print("RENOVATION is ", reserve_brand, reserve_model)
        # print("RENOVATION is ", renovation_brand, renovation_model)
        # In order get right rowspan of table in department section we minus one from max
        tab_row = max([len(counting_model), len(reserve_model), len(renovation_model)]) - 1
        report.append({
            # MAX NUMBER OR ROW OF DEPARTMENT TABLE
            'tab_row': tab_row,
            # ID DEP
            'dep_unique_id': dep.name,
            # 0 Штат ПЧ (СПЧ,ПП)
            'num_fighter': dep.number_fighters,
            # 1 В карауле по списку л/с
            'karaul_list': line_note_staff_base.filter(department=dep).count(),
            # 2 Налицо личного состава (Всего)
            'karaul_all': line_note_staff_base.filter(department=dep, status=None).count(),
            # 3 Налицо личного состава (Расчет)
            'karaul_fighter': line_note_staff_base.filter(department=dep, status=None,
                                                          position__fire_fighter=True).count(),
            # 4 Налицо личного состава (Начальники караулов)
            'head': line_note_staff_base.filter(department=dep, status=None,
                                                position__in=head_list).count(),
            # 4 Налицо личного состава (Командиры отделений)
            'commander': line_note_staff_base.filter(department=dep, status=None,
                                                     position__in=commander_list).count(),
            # 5 Налицо личного состава (Водители)
            'drivers': line_note_staff_base.filter(department=dep, status=None,
                                                   position=driver).count(),
            # 6 Налицо личного состава (Пожарные)
            'fire_fighter': line_note_staff_base.filter(department=dep, status=None,
                                                        position=fire_fighter).count(),
            # 7 Налицо личного состава (Диспетчеров (радиотелефонистов))
            'call_assistant': line_note_staff_base.filter(department=dep, status=None,
                                                          position=call_assistant).count(),
            # 8 Газодымозащитники/ аппараты (те кто имеет допук для работы в противогазе, включая  начальников)
            'gdzs': line_note_staff_base.filter(department=dep, status=None, gdzs=True).count(),
            # 9 Отсутствуют (Отпуск учебный/декрет.)
            'vacation': line_note_staff_base.filter(department=dep, status=vacation).count(),
            # 10 Отсутствуют (Больные)
            'sick': line_note_staff_base.filter(department=dep, status=sick).count(),
            # 11 Отсутствуют (Командировка)
            'business_trip': line_note_staff_base.filter(department=dep, status=business_trip).count(),
            # 12 Отсутствуют (Другие причины)
            'others': line_note_staff_base.filter(department=dep, status=others).count(),
            # 13 Пожарная техника (В расчете(Тип основного пожарного автомобиля))
            'counting_brand': counting_brand,
            # 14 Пожарная техника (В расчете(Марка специального.пожарного автомобиля))
            'counting_model': counting_model,
            # 15 Пожарная техника (В резерве(Тип основного пожарного автомобиля))
            'reserve_brand': reserve_brand,
            # 16 Пожарная техника (В резерве(Марка специального.пожарного автомобиля))
            'reserve_model': reserve_model,
            # 17 Пожарная техника (На ремонте(Тип основного пожарного автомобиля))
            'renovation_brand': renovation_brand,
            # 18 Пожарная техника (На ремонте(Марка специального.пожарного автомобиля))
            'renovation_model': renovation_model,
        })

    if report:
        dest_filename = create_report_line_note(date_insert, report)
        fl = open(os.path.join(settings.MEDIA_ROOT, dest_filename), 'rb')
        response = FileResponse(fl)
        return response
    else:
        return Response(".xlsx is empty")


@swagger_auto_schema(
    methods=['GET', ],
    operation_description='Получение отчета по строевым запискам',
    manual_parameters=[
        openapi.Parameter(
            'date_insert',
            in_=openapi.IN_PATH,
            description='Дата отчета',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: "ok",
    }
)
@api_view(['GET'])
def line_note_table(request, date_insert):
    # LINE NOTE OF STAFF
    line_note_staff_base = LineNoteMan.objects.filter(date_line_note=date_insert, position__main_position=False,
                                                      staff__department__city=request.user.city)
    # LINE NOTE OF TRANSPORT
    line_note_transport = LineNoteTrans.objects.filter(date_line_note=date_insert,
                                                       department__city=request.user.city)
    departments = FireDepartment.objects.filter(city=request.user.city).order_by('name')

    report = list()
    # Для 3 Налицо личного состава (Начальники караулов)
    head_list = [pos.id for pos in Position.objects.filter(name__startswith='Начальник')]
    # Для 4 Налицо личного состава (Командиры отделений)
    commander_list = [pos.id for pos in Position.objects.filter(name__startswith='Командир')]
    # Для 5 Налицо личного состава (Водители)
    driver = Position.objects.get(name='Водитель')
    # Для 6 Налицо личного состава (Пожарный)
    fire_fighter = Position.objects.get(name='Пожарный')
    # Для 7 Налицо личного состава (Диспетчеров (радиотелефонистов))
    call_assistant = Position.objects.get(name='Диспетчер')
    # Для 9 Отсутствуют (Отпуск учебный/декрет.)
    vacation = Status.objects.get(status='Отпуск')
    # Для 10 Отсутствуют (Больные)
    sick = Status.objects.get(status='Больничный')
    # Для 11 Отсутствуют (Командировка)
    business_trip = Status.objects.get(status='Командировка')
    # Для 12 Отсутствуют (Другие причины)
    others = Status.objects.get(status='Другие причины')
    # Для 15 Пожарная техника (В резерве(Тип основного пожарного автомобиля))
    # Для 16 Пожарная техника (В резерве(Марка специального.пожарного автомобиля))
    reserve_status = TransStatus.objects.get(status='В резерве')
    # Для 17 Пожарная техника (На ремонте(Тип основного пожарного автомобиля))
    # Для 18 Пожарная техника (На ремонте(Марка специального.пожарного автомобиля))
    renovation_status = TransStatus.objects.get(status='На ремонте')
    for dep in departments:
        # 13 Пожарная техника (В расчете(Тип основного пожарного автомобиля))
        counting_brand = [line.transport.brand.brand for line in line_note_transport.filter(department=dep,
                                                                                            trans_status__status="В расчете")]
        # 14 Пожарная техника (В расчете(Марка специального.пожарного автомобиля))
        counting_model = [line.transport.trans_model.model for line in
                          line_note_transport.filter(department=dep, trans_status__status="В расчете")]
        # 15 Пожарная техника (В резерве(Тип основного пожарного автомобиля))
        reserve_brand = [line.transport.brand.brand for line in line_note_transport.filter(department=dep,
                                                                                           trans_status=reserve_status)]
        # 16 Пожарная техника (В резерве(Марка специального.пожарного автомобиля))
        reserve_model = [line.transport.trans_model.model for line in line_note_transport.filter(department=dep,
                                                                                                 trans_status=
                                                                                                 reserve_status)]
        # 17 Пожарная техника (На ремонте(Тип основного пожарного автомобиля))
        renovation_brand = [line.transport.brand.brand for line in line_note_transport.filter(department=dep,
                                                                                              trans_status=
                                                                                              renovation_status)]
        # 18 Пожарная техника (На ремонте(Марка специального.пожарного автомобиля))
        renovation_model = [line.transport.trans_model.model for line in
                            line_note_transport.filter(department=dep, trans_status=renovation_status)]
        # print('MAXIMUM IS ', max([len(counting_brand), len(reserve_model), len(renovation_model)]))
        # print("RENOVATION is ", counting_brand, counting_model)
        # print("RENOVATION is ", reserve_brand, reserve_model)
        # print("RENOVATION is ", renovation_brand, renovation_model)
        # In order get right rowspan of table in department section we minus one from max
        tab_row = max([len(counting_model), len(reserve_model), len(renovation_model)]) - 1
        report.append({
            # MAX NUMBER OR ROW OF DEPARTMENT TABLE
            'tab_row': tab_row,
            # ID DEP
            'dep_unique_id': dep.name,
            # 0 Штат ПЧ (СПЧ,ПП)
            'num_fighter': dep.number_fighters,
            # 1 В карауле по списку л/с
            'karaul_list': line_note_staff_base.filter(department=dep).count(),
            # 2 Налицо личного состава (Всего)
            'karaul_all': line_note_staff_base.filter(department=dep, status=None).count(),
            # 3 Налицо личного состава (Расчет)
            'karaul_fighter': line_note_staff_base.filter(department=dep, status=None,
                                                          position__fire_fighter=True).count(),
            # 4 Налицо личного состава (Начальники караулов)
            'head': line_note_staff_base.filter(department=dep, status=None,
                                                position__in=head_list).count(),
            # 4 Налицо личного состава (Командиры отделений)
            'commander': line_note_staff_base.filter(department=dep, status=None,
                                                     position__in=commander_list).count(),
            # 5 Налицо личного состава (Водители)
            'drivers': line_note_staff_base.filter(department=dep, status=None,
                                                   position=driver).count(),
            # 6 Налицо личного состава (Пожарные)
            'fire_fighter': line_note_staff_base.filter(department=dep, status=None,
                                                        position=fire_fighter).count(),
            # 7 Налицо личного состава (Диспетчеров (радиотелефонистов))
            'call_assistant': line_note_staff_base.filter(department=dep, status=None,
                                                          position=call_assistant).count(),
            # 8 Газодымозащитники/ аппараты (те кто имеет допук для работы в противогазе, включая  начальников)
            'gdzs': line_note_staff_base.filter(department=dep, status=None, gdzs=True).count(),
            # 9 Отсутствуют (Отпуск учебный/декрет.)
            'vacation': line_note_staff_base.filter(department=dep, status=vacation).count(),
            # 10 Отсутствуют (Больные)
            'sick': line_note_staff_base.filter(department=dep, status=sick).count(),
            # 11 Отсутствуют (Командировка)
            'business_trip': line_note_staff_base.filter(department=dep, status=business_trip).count(),
            # 12 Отсутствуют (Другие причины)
            'others': line_note_staff_base.filter(department=dep, status=others).count(),
            # 13 Пожарная техника (В расчете(Тип основного пожарного автомобиля))
            'counting_brand': counting_brand,
            # 14 Пожарная техника (В расчете(Марка специального.пожарного автомобиля))
            'counting_model': counting_model,
            # 15 Пожарная техника (В резерве(Тип основного пожарного автомобиля))
            'reserve_brand': reserve_brand,
            # 16 Пожарная техника (В резерве(Марка специального.пожарного автомобиля))
            'reserve_model': reserve_model,
            # 17 Пожарная техника (На ремонте(Тип основного пожарного автомобиля))
            'renovation_brand': renovation_brand,
            # 18 Пожарная техника (На ремонте(Марка специального.пожарного автомобиля))
            'renovation_model': renovation_model,
        })

    return Response(report)