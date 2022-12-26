from django.urls import path
from django.contrib.auth.views import PasswordChangeView
from . import views


urlpatterns = [
    path('old_map/', views.test, name='old_map'),
    path('', views.current_emergency, name='current_appeal'),
    path('close-emergency/<int:emergency_id>/', views.close_emergency, name='close_emergency'),
    
    path('edit/<int:cur_emg_id>/', views.current_emergency_edit, name='current_emergency_edit'),



    path('archive/', views.current_appear_archive, name='current_appear_archive'),
    path('current-emergencies/', views.current_appear_archive, name='current_emergencies'),


    path('get_emergency_boss/', views.get_emergency_boss, name='get_emergency_boss'),
    path('get_emergency_transport/', views.get_emergency_transport, name='get_emergency_transport'),

    path('journal-event/<int:pk>/<str:status>/', views.journal_event, name='journal_event'),
    path('download/<int:pk>/', views.download_file, name='download_report'),
    path('line-note/', views.line_note, name='line_note'),
    path('line-note-main/<str:date_insert>/', views.line_note_main, name='line_note_main'),
    path('line-note-record/<str:date_insert>/', views.line_note_record, name='line_note_record'),
    path('line-note-report/<str:date_insert>/', views.line_note_report, name='line_note_report'),
    path('statistics/', views.statistics, name='statistics'),
    path('stat_pdf/', views.GeneratePdf.as_view(), name='stat_pdf'),
    path('income-voice-record/', views.income_voice_record, name='income_voice_record'),
    path('knowledge-storage/', views.knowledge_storage, name='knowledge_storage'),
    path('knowledge-storage/<str:section>', views.knowledge_section, name='knowledge_section'),
    path('api/new_income_call/', views.new_income_call),
    path('api/new_income_call_end_time/', views.new_income_call_end_time),
    path('api/mark_quality/', views.mark_quality),
    path('logout/', views.logout, name='logout'),
    path('report-excel/', views.reportExcel, name='report_excel'),
    path('know/', views.knowledge_base, name='knowledge_base'),
    path('profile/', views.profileInfo, name='profile'),
    path('map/', views.map, name='map'),
    path('line-note-history/', views.line_note_history, name='not-history'),

]
