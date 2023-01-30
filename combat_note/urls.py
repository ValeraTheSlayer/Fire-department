from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('line_note_man', views.LineNoteManViewSet)
router.register('line_note_transport', views.LineNoteTransViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('line_note_report/excel/<str:date_insert>/', views.line_note_report, name='line_note_excel'),
    path('line_note_report/table/<str:date_insert>/', views.line_note_table, name='line_note_table'),

]
