# -*- coding: utf-8 -*-
import json
from django.contrib.auth.models import User
from django.db.models import Count, Max
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
import emergency
from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime, timedelta, date
from .forms import *
from .filters import *
from .report import create_report, create_report_emergency
import os
import pandas as pd
from io import BytesIO
from .schedule import scheduler
from paramiko import SSHClient
from scp import SCPClient
from combat_note.models import LineNoteMan, LineNoteTrans
from transport.models import Transport, TransStatus
from personnel.models import  Staff, Sentry, Position, Status

from emergency.filters import CurrentEmergencyFilter

from django.http import JsonResponse

from django.views.generic import View
from .process import html_to_pdf

#from .models import DefaultEvent, JournalEvent
# from emergency.models import JournalEvent, DefaultEvent
#from emergency.filters import CurrentEmergencyFilter

from .forms import TransportForm



channel_layer = get_channel_layer()

# REMOTE SERVER OF ASTERISK
SERVER = '10.180.210.87'
USERNAME = 'root'
PASSWORD = 'passw0rd13!'


channel_layer = get_channel_layer()


def test(request):
    return render(request, 'application/5_map.html')


def download_file(request, pk):
    cur_emg = CurrentAppeal.objects.get(id=pk)
    event_journal = JournalEvent.objects.filter(emergency=cur_emg)
    dest_filename = create_report_emergency(cur_emg, event_journal)
    # fill these variables with real values
    fl = open(dest_filename, 'rb')
    response = FileResponse(fl)
    return response

def save_income_voice(unique_id):
    #print(datetime.now())
    data = ApiData.objects.get(unique_id=unique_id)
    date_of_call = str(data.start_time.date()).replace('-', '/')
    ssh = SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect(SERVER, username=USERNAME, password=PASSWORD)
    ftp = ssh.open_sftp()
    path_folder = '/var/spool/asterisk/monitor/' + date_of_call + '/'
    # path_folder = '/var/spool/asterisk/monitor/' + '2021/10/21' + '/'
    files = ftp.listdir(
        path_folder)
    for file in files:
        audio_file = file.split('-')[-1]
        if unique_id + '.wav' == audio_file:
            with SCPClient(ssh.get_transport()) as scp:
                scp.get(path_folder + file,
                        'application/static/audio/' + audio_file)
            data.downloaded = True
            data.save()

@login_required(login_url='/accounts/login/')
def current_emergency(request):
    user_ = UserInfo.objects.get(user=request.user)
    appeal_id_of_modal = None
    count_call_number_modal = None
    # GIVEN ANSWER TO QUESTION
    if 'answer_to_short_question' in request.POST:
        answer_to_short_question = request.POST.get('answer_to_short_question')
        appeal_id_of_modal_after_answer = request.POST.get('appeal_modal_id_is')
        responsible_department_person_modal = request.POST.get('responsible_department_person_modal')
        callback_number_modal = request.POST.get('callback_number_modal', None)
        citizenship_modal = request.POST.get('citizenship_modal')
        iin_modal = request.POST.get('iin_modal')
        street_modal = request.POST.get('street_modal')
        house_modal = request.POST.get('house_modal')
        flat_modal = request.POST.get('flat_modal')
        email_modal = request.POST.get('email_modal')
        if callback_number_modal == "":
            callback_number_modal = None
        # print(appeal_id_of_modal_after_answer,
        #       answer_to_short_question,
        #       responsible_department_person_modal,
        #       callback_number_modal,
        #       citizenship_modal,
        #       iin_modal,
        #       street_modal,
        #       house_modal,
        #       flat_modal,
        #       email_modal
        #       )

        if answer_to_short_question and responsible_department_person_modal:
            appeal = CurrentAppeal.objects.get(id=int(appeal_id_of_modal_after_answer))
            appeal.answer_to_short_question = answer_to_short_question
            appeal.responsible_department_person = responsible_department_person_modal
            appeal.callback_number = callback_number_modal
            appeal.iin = iin_modal
            appeal.street = street_modal
            appeal.house = house_modal
            appeal.flat = flat_modal
            appeal.email = email_modal
            # APPEAL WAS SOLVED
            appeal.status = True
            appeal.save()
    # OPEN MODAL WITH CONTENT THIS APPEAL
    if 'appeal_input_id' in request.POST:
        appeal_id_of_modal = int(request.POST.get('appeal_input_id').split('_')[1])
        count_call_number_modal = len(CurrentAppeal.objects.filter(income_call_number=CurrentAppeal.objects.get(id=appeal_id_of_modal).income_call_number))

    # CREATED NEW APPEAL
    if 'short_question' in request.POST:
        short_question = request.POST.get('short_question')
        date_of_call = request.POST.get('date_of_call')
        time_of_call = request.POST.get('time_of_call')
        time_of_call_end = request.POST.get('time_of_call_end')
        income_call_number = request.POST.get('income_call_number', None)
        callback_number = request.POST.get('callback_number', None)
        income_call_name = request.POST.get('income_call_name')
        citizenship = request.POST.get('citizenship')
        iin = request.POST.get('iin')
        borderpost = request.POST.get('borderpost')
        city = request.POST.get('city')
        street = request.POST.get('street')
        house = request.POST.get('house')
        flat = request.POST.get('flat')
        email = request.POST.get('email')
        question_category = request.POST.get('question_category')
        status = request.POST.get('status')

        responsible_department_person = request.POST.get('responsible_department_person')
        address = request.POST.get('address')
        emergency_rank = request.POST.get('emergency_rank')
        object_owner = request.POST.get('object_owner')
        emergency_type = request.POST.get('emergency_type')
        object_category = request.POST.get('object_category')

        department = request.POST.getlist('department')
        transport = request.POST.getlist('transport')

        if request.POST.get('api_unique_id') == '':
            date_of_call = str(datetime.now().date().strftime("%d.%m.%Y"))
            time_of_call = str(datetime.now().time().strftime("%H:%M:%S"))

            try:
                unique_id = float(ApiData.objects.all().order_by('-unique_id')[0].unique_id) + 1
            except:
                unique_id = 1

            api = ApiData.objects.create(
                start_time=datetime.strptime(date_of_call + ' ' + time_of_call, '%d.%m.%Y %H:%M:%S'),
                number_in=income_call_number,
                user=user_,
                unique_id=str(unique_id),
                )
            api_unique_id = api.unique_id
        else:
            api_unique_id = request.POST.get('api_unique_id')

        if callback_number == "":
            callback_number = None
        if income_call_number == "":
            income_call_number = None
        # Time handling
        if not time_of_call_end:
            time_of_call_end = time_of_call
        date_time_of_call_start = datetime.strptime(date_of_call + ' ' + time_of_call, '%d.%m.%Y %H:%M:%S')
        date_time_of_call_end = datetime.strptime(date_of_call + ' ' + time_of_call_end, '%d.%m.%Y %H:%M:%S')
        # Post and city handling
        if borderpost:
            borderpost = BorderPost.objects.get(id=int(borderpost))
        if city:
            city = City.objects.get(id=int(city))
        # Status of question DONE / SEND TO DEPARTMENT
        # if status:
        #     # By Default Status always True (It's means problem was solved/done)
        #     status = False
        #     responsible_depart = 'd'
        # else:
        #     status = True
        #     responsible_depart = 'c'
        status = False
        if emergency_rank:
            emergency_rank = EmergencyRank.objects.get(id=int(emergency_rank))
        if emergency_type:
            emergency_type = EmergencyType.objects.get(id=int(emergency_type))
        if object_category:
            try:
                object_category = ObjectCategory.objects.get(id=int(object_category))
            except:
                object_category = ObjectCategory.objects.create(name=object_category)

        if responsible_department_person:
            person = Staff.objects.get(id=int(responsible_department_person))
            responsible_department_person = person.full_name

        responsible_depart = 'c'
        # print(responsible_depart)
        # print(status)

        b = CurrentAppeal(
            user_created_event=user_,
            date_of_call_start=date_time_of_call_start,
            date_of_call_end=date_time_of_call_end,
            income_call_number=income_call_number,
            callback_number=callback_number,
            income_call_name=income_call_name,
            citizenship=citizenship,
            iin=iin,
            borderpost=borderpost,
            city=city,
            street=street,
            house=house,
            flat=flat,
            email=email,
            question_category=QuestionCategory.objects.get(id=int(question_category)),
            short_question=short_question,
            responsible_department=responsible_depart,
            status=status,
            api_unique_id=ApiData.objects.get(unique_id=api_unique_id),

            address=address,
            emergency_rank=emergency_rank,
            object_owner=object_owner,
            emergency_type=emergency_type,
            object_category=object_category,
            responsible_department_person=responsible_department_person,


        )
        b.save()
        if department:
            for  item in department:
                b.department.add(FireDepartment.objects.get(id=int(item)))
        if transport:
            for item in transport:
                b.transport.add(Transport.objects.get(id=int(item)))
                #department_list.append(FireDepartment.objects.get(id=int(item)))
        return redirect('current_emergencies')

    city = City.objects.all()
    borderpost = BorderPost.objects.all()
    cur_appeal = CurrentAppeal.objects.all().order_by('-id')
    # cur_appeal_not_answered = CurrentAppeal.objects.filter(status=False).order_by('-id')
    # cur_appeal_answered = CurrentAppeal.objects.filter(status=True).order_by('-id')
    # cur_appeal_union = list(cur_appeal_not_answered) + list(cur_appeal_answered)
    cur_appeal_filter = CurrentAppealFilter(request.GET, queryset=cur_appeal)

    paginator = Paginator(cur_appeal_filter.qs, 5)
    page = request.GET.get('page', 1)
    try:
        cur_appeal = paginator.page(page)
    except PageNotAnInteger:
        cur_appeal = paginator.page(1)
    except EmptyPage:
        cur_appeal = paginator.page(paginator.num_pages)

    question_category = QuestionCategory.objects.all()
    # USER OPEN MODAL WITH CONTENT OF APPEAL
    if appeal_id_of_modal:
        cur_appeal_modal = CurrentAppeal.objects.get(id=appeal_id_of_modal)
    else:
        cur_appeal_modal = appeal_id_of_modal


    transport = Transport.objects.all()
    departaments = FireDepartment.objects.all()




    bosses = Staff.objects.filter(position__name='Начальник')
    # boss = LineNoteMan.objects.get(date_line_note=datetime.now().date(), position__name = 'Начальник')



    emergency_types = EmergencyType.objects.all()
    object_categories = ObjectCategory.objects.all()
    emergency_ranks = EmergencyRank.objects.all()


    diff_time = timedelta(hours=1)
    return render(request, 'application/1_current_appeal.html', {
        'diff_time': diff_time,
        'cur_appeal': cur_appeal,
        'cur_appeal_filter': cur_appeal_filter,
        'city': city,
        'borderpost': borderpost,
        'question_category': question_category,
        'cur_appeal_modal': cur_appeal_modal,
        'count_call_number_modal': count_call_number_modal,
        'departaments' : departaments,
        'transport': transport,
        'bosses': bosses,
        #'boss': boss,
        'emergency_types' : emergency_types,
        'object_categories' : object_categories,
        'emergency_ranks': emergency_ranks,
        #'object_owner': object_owner,
    })



@login_required(login_url='/accounts/login/')
def current_appear_archive(request):

    user_ = UserInfo.objects.get(user=request.user)

    date_for_search = date.today()
    if request.path == '/main_page/archive/':
        cur_emg = CurrentAppeal.objects.filter(user_created_event__city=user_.city,
            date_of_call_start__lte = date_for_search
        ).order_by('-id')
    else:
        #date_for_search = datetime.today() - timedelta(days=2)

        cur_emg = CurrentAppeal.objects.filter(user_created_event__city=user_.city,
                  date_of_call_start__contains = date_for_search
                  ).order_by('-id')
        #print(date_for_search)

    date_range_filter = request.GET.get('dateRangeFilter')
    datetime_before, datetime_after = None, None
    if date_range_filter:
        datetime_before = datetime.strptime(date_range_filter.split(' - ')[0], '%d/%m/%Y %H:%M')
        datetime_after = datetime.strptime(date_range_filter.split(' - ')[1], '%d/%m/%Y %H:%M')
        cur_emg = cur_emg.filter(date_of_call_start__range=[datetime_before, datetime_after])

    cur_filter = CurrentEmergencyFilter(request.GET, queryset=cur_emg)


    # cur_appeal = CurrentAppeal.objects.all().order_by('-id')
    # cur_appeal_filter = CurrentAppealFilter(request.GET, queryset=cur_appeal)
    # paginator = Paginator(cur_appeal_filter.qs, 5)
    # page = request.GET.get('page', 1)
    # try:
    #     cur_appeal = paginator.page(page)
    # except PageNotAnInteger:
    #     cur_appeal = paginator.page(1)
    # except EmptyPage:
    #     cur_appeal = paginator.page(paginator.num_pages)



    question_category = QuestionCategory.objects.all()
    transport = Transport.objects.all()
    departaments = FireDepartment.objects.all()
    question_category = QuestionCategory.objects.all()
    bosses = Staff.objects.filter(position__name='Начальник')

    emergency_types = EmergencyType.objects.all()
    object_categories = ObjectCategory.objects.all()
    emergency_ranks = EmergencyRank.objects.all()
    transport = Transport.objects.all()

    return render(request, 'application/1_current_emergency_archive.html', {
        'filter': cur_filter,
        'datetime_before': datetime_before,
        'datetime_after': datetime_after,
        'departaments' : departaments,
        'transport': transport,
        'bosses': bosses,
        'emergency_types' : emergency_types,
        'object_categories' : object_categories,
        'emergency_ranks': emergency_ranks,
        'question_category': question_category,
        'transport': transport,

    })

def current_emergiencies(request):

    return render(request, 'application/current_emergencies.html', context={})

@login_required(login_url='/accounts/login/')
def current_emergency_edit(request, cur_emg_id):
    cur_emg = CurrentAppeal.objects.get(id=cur_emg_id)
    if request.method == 'POST':
        form = CurrentEmergencyForm(request.POST, cur_emg)
        if form.is_valid():
            cur_emg.income_call_number = request.POST.get('income_call_number')
            cur_emg.income_call_name = request.POST.get('income_call_name')
            cur_emg.address = request.POST.get('address')
            cur_emg.house_kv = request.POST.get('house_kv')
            cur_emg.emergency_type = EmergencyType.objects.get(id=int(request.POST.get('emergency_type')))
            cur_emg.emergency_rank = EmergencyRank.objects.get(id=int(request.POST.get('emergency_rank')))
            department = request.POST.getlist('department')
            cur_emg.department.clear()
            for dep in department:
                dp = FireDepartment.objects.get(id=int(dep))

                cur_emg.department.add(dp)

            cur_emg.first_info_burning = request.POST.get('first_info_burning')
            staff = request.POST.get('staff')
            cur_emg.staff = staff

            transport = request.POST.getlist('transport')
            cur_emg.transport.clear()
            for trans in transport:
                tr = Transport.objects.get(id=int(trans))
                cur_emg.transport.add(tr)

            cur_emg.save()
            return redirect('current_appear_archive')
    form = CurrentEmergencyForm(instance=cur_emg)

    return render(request, 'application/1_current_emergency_edit.html', {
        'form': form,
        'cur_emg_id': cur_emg_id
    })


@login_required(login_url='/accounts/login/')
def journal_event(request, pk, status):
    cur_emg = CurrentAppeal.objects.get(id=pk)
    form = None
    if 'edit' in request.GET:
        event_id = int(request.GET.get('edit'))
        try:
            event = JournalEvent.objects.get(id=event_id)
            form = JournalEventForm(instance=event)
            if request.method == 'POST':
                form = JournalEventForm(request.POST, event)
                if form.is_valid():
                    event.event = request.POST.get('event')
                    event.save()
                    form = None
        except JournalEvent.DoesNotExist:
            pass
    if 'delete' in request.GET:
        event_id = int(request.GET.get('delete'))
        try:
            event = JournalEvent.objects.get(id=event_id)
            event.delete()
        except JournalEvent.DoesNotExist:
            pass
    if 'new_event' in request.POST:
        date_insert = datetime.now()
        new_event = request.POST.get('new_event')
        b = JournalEvent(emergency=cur_emg, event=new_event, date_insert=date_insert)
        b.save()
    default_events = DefaultEvent.objects.all()
    event_list = JournalEvent.objects.filter(emergency=cur_emg).order_by('-id')
    return render(request, 'application/1_journal_event.html', {
        'default_events': default_events,
        'event_list': event_list,
        'status': status,
        'form': form
    })


@login_required(login_url='/accounts/login/')
def line_note(request):

    userinfo = UserInfo.objects.get(user=request.user)

    if 'date_line_note' in request.POST:
        date_insert = request.POST.get('date_line_note')
        if userinfo.user.username.startswith("pozh"):
            # HERE USER CAN EDIT ONLY TODAY AND AT CERTAIN TIME
            if date_insert == str(datetime.now().date()):
                return redirect('line_note_main', date_insert=date_insert)
            else:
                if not (LineNoteMan.objects.filter(date_line_note=date_insert, position__main_position=False) or
                        LineNoteTrans.objects.filter(date_line_note=date_insert)):
                    return render(request, 'application/2_line_note.html', {
                        'userinfo': userinfo,
                        'warning': 'Нету данных'
                    })
                else:
                    return redirect('line_note_record', date_insert=date_insert)
        elif userinfo.user.has_perm('application.user_main_call_center_city'):
            return redirect('line_note_report', date_insert=date_insert)

    return render(request, 'application/2_line_note.html', {
        'userinfo': userinfo
    })



@login_required(login_url='/accounts/login/')
def line_note_report(request, date_insert):
    userinfo = UserInfo.objects.get(user=request.user)
    # LINE NOTE OF STAFF
    line_note_staff_base = LineNoteMan.objects.filter(date_line_note=date_insert, position__main_position=False,
                                                      staff__department__city=userinfo.city.id)
    # LINE NOTE OF TRANSPORT
    line_note_transport = LineNoteTrans.objects.filter(date_line_note=date_insert,
                                                       department__city=userinfo.city.id)
    departments = FireDepartment.objects.filter(city=userinfo.city.id)

    report = list()
    # Для 3 Налицо личного состава (Начальники караулов)
    head_list = [pos.id for pos in Position.objects.filter(name__startswith='НАЧАЛЬНИК')]
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
    others = Status.objects.get(status='Дригие причины')
    # Для 15 Пожарная техника (В резерве(Тип основного пожарного автомобиля))
    # Для 16 Пожарная техника (В резерве(Марка специального.пожарного автомобиля))
    reserve_status = TransStatus.objects.get(status='В резерве')
    # Для 17 Пожарная техника (На ремонте(Тип основного пожарного автомобиля))
    # Для 18 Пожарная техника (На ремонте(Марка специального.пожарного автомобиля))
    renovation_status = TransStatus.objects.get(status='На ремонте')
    for dep in departments:
        # 13 Пожарная техника (В расчете(Тип основного пожарного автомобиля))
        counting_brand = [line.transport.brand.brand for line in line_note_transport.filter(department=dep,
                                                                                            trans_status=None)]
        # 14 Пожарная техника (В расчете(Марка специального.пожарного автомобиля))
        counting_model = [line.transport.trans_model.model for line in
                          line_note_transport.filter(department=dep, trans_status=None)]
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
            'dep_unique_id': dep.name, #id
            # 0 Штат ПЧ (СПЧ,ПП)
            'num_fighter': dep.number_fighters,
            # 1 В карауле по списку л/с
            'karaul_list': line_note_staff_base.filter(staff__department=dep).count(),
            # 2 Налицо личного состава (Всего)
            'karaul_all': line_note_staff_base.filter(staff__department=dep, status=None).count(),
            # 3 Налицо личного состава (Расчет)
            'karaul_fighter': line_note_staff_base.filter(staff__department=dep, status=None,
                                                          position__fire_fighter=True).count(),
            # 4 Налицо личного состава (Начальники караулов)
            'head': line_note_staff_base.filter(staff__department=dep, status=None,
                                                position__in=head_list).count(),
            # 4 Налицо личного состава (Командиры отделений)
            'commander': line_note_staff_base.filter(staff__department=dep, status=None,
                                                     position__in=commander_list).count(),
            # 5 Налицо личного состава (Водители)
            'drivers': line_note_staff_base.filter(staff__department=dep, status=None,
                                                   position=driver).count(),
            # 6 Налицо личного состава (Пожарные)
            'fire_fighter': line_note_staff_base.filter(staff__department=dep, status=None,
                                                        position=fire_fighter).count(),
            # 7 Налицо личного состава (Диспетчеров (радиотелефонистов))
            'call_assistant': line_note_staff_base.filter(staff__department=dep, status=None,
                                                          position=call_assistant).count(),
            # 8 Газодымозащитники/ аппараты (те кто имеет допук для работы в противогазе, включая  начальников)
            'gdzs': line_note_staff_base.filter(staff__department=dep, status=None, gdzs=True).count(),
            # 9 Отсутствуют (Отпуск учебный/декрет.)
            'vacation': line_note_staff_base.filter(staff__department=dep, status=vacation).count(),
            # 10 Отсутствуют (Больные)
            'sick': line_note_staff_base.filter(staff__department=dep, status=sick).count(),
            # 11 Отсутствуют (Командировка)
            'business_trip': line_note_staff_base.filter(staff__department=dep, status=business_trip).count(),
            # 12 Отсутствуют (Другие причины)
            'others': line_note_staff_base.filter(staff__department=dep, status=others).count(),
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

    # print(report)
    if report:
        [os.remove('application/static/report/' + foo) for foo in os.listdir('application/static/report/')]
        create_report(date_insert, report)
    print('report',report)
    return render(request, 'application/2_line_note_report.html', {
        'userinfo': userinfo,
        'date_insert': date_insert,
        'line_note_staff_base': line_note_staff_base,
        'line_note_transport': line_note_transport,
        'report': report
    })


@login_required(login_url='/accounts/login/')
def line_note_record(request, date_insert):
    userinfo = UserInfo.objects.get(user=request.user)
    # LINE NOTE OF STAFF
    line_note_staff_base = LineNoteMan.objects.filter(date_line_note=date_insert,
                                                      staff__department=userinfo.department)
    # LINE NOTE OF TRANSPORT
    line_note_transport = LineNoteTrans.objects.filter(date_line_note=date_insert,
                                                       department=userinfo.department). \
        order_by('transport__id')

    return render(request, 'application/2_line_note_record.html', {
        'userinfo': userinfo,
        'date_insert': date_insert,
        'line_note_staff_base': line_note_staff_base,
        'line_note_transport': line_note_transport,
    })


@permission_required('application.user_fire_department_call_center')
@login_required(login_url='/accounts/login/')
def line_note_main(request, date_insert):
    warning = None

    userinfo = UserInfo.objects.get(user=request.user)
    if date_insert != str(datetime.now().date()):
        return redirect('line_note')

    if 'new_number' in request.POST:
        transform = TransportForm(request.POST)
        if transform.is_valid():
            if transform.cleaned_data['brand']:
                transform.save()
        else:
            warning = transform.errors
    if 'selected_trans_status' in request.POST:
        selected_trans_status = (request.POST.get('selected_trans_status')).split(',')
        for sts in selected_trans_status:
            st = sts.split('|')
            # Get transport status
            if st[1] != "None":
                trans_status = TransStatus.objects.get(id=int(st[1]))
            else:
                trans_status = None
            # HERE GET WHAT TRANSPORT MODIFICATION DOING NOW
            transport = Transport.objects.get(id=int(st[0]))

            try:
                line = LineNoteTrans.objects.get(date_line_note=date_insert,
                                                 department=userinfo.department,
                                                 transport=transport)
                line.trans_status = trans_status
                line.save()
            except LineNoteTrans.DoesNotExist:
                line = LineNoteTrans(date_line_note=date_insert,
                                     department=userinfo.department,
                                     transport=transport,
                                     trans_status=trans_status)
                line.save()

    if 'staff_unique_id' in request.POST:
        staff_unique_id = request.POST.get('staff_unique_id')
        staff_full_name = request.POST.get('staff_full_name')
        staff_position = request.POST.get('staff_position')
        staff_position = Position.objects.get(id=int(staff_position))
        staff_karaul = request.POST.get('staff_karaul')
        staff_gdzs = request.POST.get('staff_gdzs')
        print(staff_karaul)
        sentry = Sentry.objects.get(id=staff_karaul)
        print(sentry)

        s = Staff(unique_id=staff_unique_id,
                  full_name=staff_full_name,
                  position=staff_position,
                  department=userinfo.department,
                  sentry=sentry,
                  gdzs=staff_gdzs)
        existing_user_len = len(Staff.objects.filter(unique_id=staff_unique_id))
        if existing_user_len == 0:
            s.save()


    if request.method == "POST" and request.is_ajax and request.is_ajax and 'selected_position' in request.POST:
        department = userinfo.department
        selected_position_list = json.loads(request.POST.get('selected_position'))
        print('request', request.POST)
        for person in selected_position_list:
            if person['selected_position'] == 'None' or person['selected_person'] == 'None':
                warning = 'Пожалуйста выберите из списка должность и ФИО'
            else:
                selected_position = Position.objects.get(id=int(person['selected_position']))
                selected_person = Staff.objects.get(id=int(person['selected_person']))
                if person['selected_status'] != 'None':

                    selected_status = Status.objects.get(id=int(person['selected_status']))
                else:
                    selected_status = None
                print(person['selected_gdzs'])
                if person['selected_gdzs'] == True:
                    selected_gdzs = True
                else:
                    selected_gdzs = False
                is_unique_for_today = True
                to_day_person_dublicetes = len(LineNoteMan.objects.filter(date_line_note=date_insert, staff=person['selected_person']))
                if to_day_person_dublicetes > 0:
                    is_unique_for_today = False
                if is_unique_for_today:
                    b = LineNoteMan(date_line_note=date_insert, position=selected_position,
                                    staff=selected_person, status=selected_status,
                                    gdzs=selected_gdzs, department=department,
                                    )
                    b.save()

    # LINE NOTE OF TRANSPORT STATUS
    line_note_transport = LineNoteTrans.objects.filter(date_line_note=date_insert,
                                                       department=userinfo.department). \
        order_by('transport__id')
    # If extra transport was added
    transports = Transport.objects.filter(department=userinfo.department)
    if line_note_transport:
        if len(transports) > len(line_note_transport):
            for new_trans in transports:
                if not line_note_transport.filter(transport=new_trans):
                    line = LineNoteTrans(date_line_note=date_insert,
                                         department=userinfo.department,
                                         transport=new_trans,
                                         trans_status=None)
                    line.save()
    # REFRESH LINE NOTE OF TRANSPORT STATUS
    line_note_transport = LineNoteTrans.objects.filter(date_line_note=date_insert,
                                                       department=userinfo.department). \
        order_by('transport__id')
    # LINE NOTE OF STAFF
    line_note_staff_base = LineNoteMan.objects.filter(date_line_note=date_insert,
                                                      staff__department=userinfo.department)
    # Exclude list of person from list of persons
    line_note_list = [st.staff.unique_id for st in line_note_staff_base]
    staff_members_base = Staff.objects.filter(department=userinfo.department, position__main_position=False)#.exclude(unique_id__in=line_note_list)


    staff_members_main = Staff.objects.filter(department=userinfo.department, unique_id__in=line_note_list)
    members_base = []

    positions = Position.objects.all()
    status = Status.objects.all()
    trans_status = TransStatus.objects.all()
    karaul = Sentry.objects.all()
    transform = TransportForm()
    all_def_staff = Staff.objects.filter(department=userinfo.department)

    return render(request, 'application/2_line_note_main.html', {
        'userinfo': userinfo,
        'date_insert': date_insert,
        'staff_members_main': staff_members_main,
        'staff_members_base': staff_members_base,
        'line_note_staff_base': line_note_staff_base,
        'line_note_transport': line_note_transport,
        'transports': transports,
        'positions': positions,
        'karaul': karaul,
        'status': status,
        'trans_status': trans_status,
        'transform': transform,
        'warning': warning,
        'all_staff': all_def_staff,
    })


@login_required(login_url='/accounts/login/')
def statistics(request):

    emergency_types = EmergencyType.objects.all()
    objects = ObjectCategory.objects.all()

    types = []
    for t in emergency_types:
        count = CurrentAppeal.objects.filter(emergency_type=t).count()
        types.append({'type': t, 'count': count})

    cats = []
    for t in objects:
        count = CurrentAppeal.objects.filter(object_category=t).count()
        cats.append({'type': t, 'count': count})
    context = {
        'types': types,
        'cats': cats
    }
    return render(request, 'application/3_statistics.html', context)



@login_required(login_url='/accounts/login/')
def knowledge_storage(request):
    all_know = KnowledgeBase.objects.all().values()
    #print(type(all_know))
    know = KnowledgeBase.objects.all().values_list('section').distinct().order_by('section')
    know = [i[0] for i in know]
    return render(request, 'application/6_knowledge_storage.html', {'know': know, 'all_know': all_know, })

@login_required(login_url='/accounts/login/')
def knowledge_section(request, section):
    all_know = KnowledgeBase.objects.filter(section=section).values()

    return render(request, 'application/6_knowledge_section.html', {'section': section, 'all_know': all_know, })



@login_required(login_url='/accounts/login/')
def income_voice_record(request):
    #print(request.POST.get('api_data_unique_id'))
    if 'api_data_unique_id' in request.POST:
        unique_id = request.POST.get('api_data_unique_id')
        data = ApiData.objects.get(unique_id=unique_id)
        date_of_call = str(data.start_time.date()).replace('-', '/')
        ssh = SSHClient()
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(SERVER, username=USERNAME, password=PASSWORD)
        ftp = ssh.open_sftp()
        path_folder = '/var/spool/asterisk/monitor/' + date_of_call + '/'
        files = ftp.listdir(
            path_folder)
        for file in files:
            audio_file = file.split('-')[-1]
            if unique_id + '.wav' == audio_file:
                with SCPClient(ssh.get_transport()) as scp:
                    scp.get(path_folder + file,
                            'application/static/audio/' + audio_file)
                data.downloaded = True
                data.save()
    api_data = ApiData.objects.all().order_by('-start_time')
    api_data_filter = ApiDataFilter(request.GET, queryset=api_data)
    return render(request, 'application/4_income_voice_record.html', {
        'api_data': api_data_filter.qs,
        'api_data_filter': api_data_filter,
    })


@api_view(['GET'])
def new_income_call_end_time(request):
    if 'end_time' in request.GET:
        end_time = datetime.now()
        unique_id = request.GET.get('unique_id')
        #print(end_time, unique_id)

        try:
            api_data = ApiData.objects.get(unique_id=unique_id)
            scheduler.add_job(save_income_voice, trigger='date', run_date=datetime.now() + timedelta(seconds=3),
                              args=(unique_id,))
            api_data.end_time = end_time
            api_data.second_api = True
            data_for_number_in = None # fix error in async socker event['data_for_number_in']
            count_call_new_appeal = None # fix error in async socker event['count_call_new_appeal']
            api_data.save()
            sip_number = api_data.user.sip_number
            user_id = UserInfo.objects.get(sip_number=sip_number).user.id
            async_to_sync(channel_layer.group_send)(str(user_id),
                                                    {'type': 'send_income_call',
                                                     'unique_id': unique_id,
                                                     'data_for_number_in': data_for_number_in,
                                                     'count_call_new_appeal': count_call_new_appeal,
                                                     'end_time': str(end_time),
                                                     'api': 2})
        except ApiData.DoesNotExist:
            #print('Unique_id does not exist!')
            pass

    data = {'success': 'yes'}
    return Response(data)


@api_view(['GET'])
def new_income_call(request):
    if 'income_number' in request.GET:

        unique_id = request.GET.get('unique_id')
        number_in = request.GET.get('income_number')
        sip_number = request.GET.get('sip_number')
        start_time = datetime.now()
        #print(unique_id,
        #      number_in,
        #      sip_number)
        try:
            user = UserInfo.objects.get(sip_number=sip_number)
            data_for_number = CurrentAppeal.objects.filter(income_call_number=number_in).order_by('-id').values("income_call_name",
                                                                                                                "iin", "short_question")
            if number_in[0] == '8':
                number_in = '7' + number_in[1:]
            # если данные по номеру есть, то
            if data_for_number:
                # беру последнюю актуальную запись
                data_for_number_in = data_for_number[0]
                count_call_new_appeal = len(data_for_number)
            else:
                data_for_number_in = None
                count_call_new_appeal = None
            b = ApiData(unique_id=unique_id, number_in=number_in,
                        user=user, start_time=start_time,
                        first_api=True)
            b.save()
            # print(user.user.id)

            async_to_sync(channel_layer.group_send)(str(user.user.id),
                                                    {'type': 'send_income_call',
                                                     'unique_id': unique_id,
                                                     'number_in': number_in,
                                                     'count_call_new_appeal': count_call_new_appeal,
                                                     'data_for_number_in': data_for_number_in,
                                                     'api': 1})
        except UserInfo.DoesNotExist:
            #print('User with this sip number does not exist')
            pass
    data = {'success': 'yes'}
    return Response(data)


@api_view(['GET'])
def mark_quality(request):
    if 'mark_quality' in request.GET:
        unique_id = request.GET.get('unique_id')
        mark_quality = request.GET.get('mark_quality')
        #print(unique_id, mark_quality)
        try:
            if mark_quality != '':
                api_data = ApiData.objects.get(unique_id=unique_id)
                api_data.mark_quality = int(mark_quality)
                api_data.save()
        except:
            #print('Doesnt exist api data')
            pass
    data = {'success': 'yes'}
    return Response(data)


def logout(request):
    logout(request)
    redirect('/')

@login_required(login_url='/accounts/login/')
def reportExcel(request):

    cur_appeals = CurrentAppeal.objects.all().order_by('id')[0:34]
    cur_appeals_filter = CurrentAppealFilter(request.GET, queryset=cur_appeals)

    time_talking = []
    operator_full_name = []
    operator_first_name = [u[0] for u in cur_appeals_filter.qs.values_list('user_created_event__user__first_name')]
    time_start_call = [u[0] for u in cur_appeals_filter.qs.values_list('date_of_call_start')]

    for i, j in enumerate(cur_appeals_filter.qs.values_list('date_of_call_end')):
        time_talking.append(j[0] - time_start_call[i])

    for i, j in enumerate(cur_appeals_filter.qs.values_list('user_created_event__user__last_name')):
        operator_full_name.append(j[0] + ' ' + operator_first_name[i])

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    data = {'Номер учетной карточки': [u[0] for u in cur_appeals_filter.qs.values_list('id')],
    'Статус звонка': ['Отвеченный']*len(operator_full_name),
    'Дата звонка': [i.strftime("%d.%m.%Y") for i in time_start_call],
    'Время звонка': [i.strftime("%H:%M:%S") for i in time_start_call],
    'Время разговора': [str(i) for i in time_talking],
    'Номер телефона': [u[0] for u in cur_appeals_filter.qs.values_list('income_call_number')],
    'Адрес': [u[0] for u in cur_appeals_filter.qs.values_list('address')],
    'Тип вызова': [u[0] for u in cur_appeals_filter.qs.values_list('emergency_type__name')],

    'Ранг': [u[0] for u in cur_appeals_filter.qs.values_list('emergency_rank')],
    'Категория объекта': [u[0] for u in cur_appeals_filter.qs.values_list('object_category__name')],

    'Пожарная часть':[u[0] for u in cur_appeals_filter.qs.values_list('department__name')],

    'Руководитель туш-я пожара': [u[0] for u in cur_appeals_filter.qs.values_list('responsible_department_person')],

    }

    df = pd.DataFrame(data)

    df.index += 1

    df.to_excel(writer, sheet_name='отчет', startrow=1, index_label='№', header=False)

    workbook = writer.book
    worksheet = writer.sheets['отчет']

    header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'border': 1})

    # Overwrite both the value and the format of each header cell
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num + 1, value, header_format)

    worksheet.write(0, 0, '№', header_format)

    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['отчет'].set_column(col_idx, col_idx, column_width)

    col_idx = df.columns.get_loc('Номер телефона')
    worksheet.set_column(col_idx+1, col_idx+1, 17)
    # col_idx = df.columns.get_loc('Категория вопроса')
    worksheet.set_column(col_idx+1, col_idx+1, 23)
    worksheet.set_column(0, 0, 5)

    writer.save()
    output.seek(0)
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=report.xlsx'

    return response

@login_required(login_url='/accounts/login/')
def knowledge_base(request):
    all_know = KnowledgeBase.objects.all().values()
    #print(type(all_know))
    know = KnowledgeBase.objects.all().values_list('section').distinct().order_by('section')
    know = [i[0] for i in know]
    return render(request, 'application/knowledge_base.html', {'know': know, 'all_know': all_know, })

@login_required(login_url='/accounts/login/')
def profileInfo(request):
    take_call = CurrentAppeal.objects.filter(user_created_event__user=request.user)
    return render(request, 'application/7_profile.html', context={'number_call': len(take_call), })

def map(request):
    return render(request, 'application/map.html')

def close_emergency(request, emergency_id):
    emergency = CurrentAppeal.objects.get(id=emergency_id)
    emergency.status = True
    emergency.save()

    return redirect('current_appear_archive')


@csrf_exempt
def get_emergency_boss(request):
    # if request.method == 'POST':
    date_insert = date.today()
    dep_list = request.POST.getlist('department[]')

    bosses_qs = Staff.objects.filter(department__id__in=dep_list, position__name='НАЧАЛЬНИК КАРАУЛА')
    today_bosses_qs = LineNoteMan.objects.filter(date_line_note=date_insert, position_id=1, department_id__in=dep_list)
    today_bosses_id = []
    for t_boss in today_bosses_qs:
        today_bosses_id.append(t_boss.staff_id)
    r = []
    for boss in bosses_qs:
        if boss.id in today_bosses_id:
            r.append({'id': boss.id, 'name': boss.full_name})

    transport_qs = Transport.objects.filter(department__id__in=dep_list)
    t = []
    for trans in transport_qs:
        t.append({'id': trans.id, 'name': trans.brand.brand + ' [' + trans.department.name + ']'})
    return JsonResponse({'bosses': r, 'transport': t})


def get_emergency_transport(request):
    return render(request, 'application/emergency_transport.html')

def stat_pdf(request):

    emergency_types = EmergencyType.objects.all()


    types = []
    for t in emergency_types:
        count = CurrentAppeal.objects.filter(emergency_type=t).count()
        types.append({'type': t, 'count': count})

    context = {
        'types': types
    }
    return render(request, 'application/stat_pdf.html', context=context)




#Creating a class based view
class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        emergency_types = EmergencyType.objects.all()


        types = []
        for t in emergency_types:
            count = CurrentAppeal.objects.filter(emergency_type=t).count()
            types.append({'type': t, 'count': count})

        context = {
            'types': types
        }
        # getting the template
        pdf = html_to_pdf('application/stat_pdf.html', context_dict=context)

         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')

@permission_required('application.user_fire_department_call_center')
@login_required(login_url='/accounts/login/')
def line_note_history(request):
    date_insert = date.today()
    userinfo = UserInfo.objects.get(user=request.user)

    line_note_staff_base = LineNoteMan.objects.filter(date_line_note=date_insert,
                                                      staff__department=userinfo.department)
    print(line_note_staff_base)
    # Exclude list of person from list of persons
    line_note_list = [st.staff.unique_id for st in line_note_staff_base]

    staff_members_main = Staff.objects.all()
    staff_members_main_1 = []
    for staff in staff_members_main:
        if staff.id in line_note_list:
            staff_members_main_1.append(staff)

    positions = Position.objects.filter(main_position=False)
    status = Status.objects.all()
    karaul = Sentry.objects.all()

    return render(request, 'application/line_note_history.html', {
        'userinfo': userinfo,
        'date_insert': date_insert,
        'staff_members_main': staff_members_main_1,
        'line_note_staff_base': line_note_staff_base,
        'line_note_list':line_note_list,
        'positions': positions,
        'karaul': karaul,
        'status': status})
