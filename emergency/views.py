import os
from django_filters import rest_framework as dj_filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from .serializers import CurrentEmergencySerializer, EmergencyTypeSerializer, EmergencyRankSerializer, \
    ObjectCategorySerializer, DefaultEventSerializer, JournalEventSerializer

from .models import CurrentEmergency, ObjectCategory, EmergencyRank, EmergencyType, DefaultEvent, JournalEvent

from .filters import BookmarkFilter, CurrentEmergencyFilter
from .services.reports import create_report_emergency
from django.conf import settings


class CurrentEmergencyViewSet(viewsets.ModelViewSet):
    """Вьюшки для поступивших заявок (форма заявки)."""
    queryset = CurrentEmergency.objects.all()
    serializer_class = CurrentEmergencySerializer
    filter_backends = [dj_filters.DjangoFilterBackend, ]
    filter_class = CurrentEmergencyFilter

    @action(detail=True, methods=('GET',), url_name='get_excel_report')
    def create_report(self, request, *args, **kwargs):
        instance = self.get_object()
        event_journal = JournalEvent.objects.filter(emergency=instance)
        dest_filename = create_report_emergency(instance, event_journal)
        fl = open(os.path.join(settings.MEDIA_ROOT, dest_filename), 'rb')
        response = FileResponse(fl)
        return response

    @action(detail=True, methods=('GET',), url_name='get_journal_event')
    def get_journal_event(self, request, *args, **kwargs):
        instance = self.get_object()
        event_journal = JournalEvent.objects.filter(emergency=instance)
        return Response(JournalEventSerializer(event_journal, many=True).data)


class EmergencyTypeViewSet(viewsets.ModelViewSet):
    """Вьюшки для типов происшествия (Пожар, и т.д.)."""
    queryset = EmergencyType.objects.all()
    serializer_class = EmergencyTypeSerializer
    filter_backends = [dj_filters.DjangoFilterBackend, ]
    filterset_fields = ['id', 'name']
    filter_class = BookmarkFilter


class EmergencyRankViewSet(viewsets.ModelViewSet):
    """Вьюшки для рангов происшествия (1, 2 и т.д.)."""
    queryset = EmergencyRank.objects.all()
    serializer_class = EmergencyRankSerializer


class ObjectCategoryViewSet(viewsets.ModelViewSet):
    """Вьюшки для категории объектов (Дом, ТЦ и т.д.)."""
    queryset = ObjectCategory.objects.all()
    serializer_class = ObjectCategorySerializer


class DefaultEventViewSet(viewsets.ModelViewSet):
    """Вьюшки по часто повторяющимся событиям в журнале событий (Пожарная бригада отправилась, и т.д.)."""
    queryset = DefaultEvent.objects.all()
    serializer_class = DefaultEventSerializer


class JournalEventViewSet(viewsets.ModelViewSet):
    """Вьюшки для журнала событий (Пожарная бригада отправилась, застряли в пробке, и т.д.)."""
    queryset = JournalEvent.objects.all()
    serializer_class = JournalEventSerializer