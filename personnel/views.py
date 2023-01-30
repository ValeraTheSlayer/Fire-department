from rest_framework import viewsets
from django_filters import rest_framework as dj_filter

from .serializers import PositionSerializer, StaffSerializer, StatusSerializer
from .filters import StaffFilter
from .models import Position, Staff, Status


class PositionViewSet(viewsets.ModelViewSet):
    """Вьюшки по существующим должностям сотрудников"""
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class StaffViewSet(viewsets.ModelViewSet):
    """Вьюшки по сотрудникам"""
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    filter_backends = [dj_filter.DjangoFilterBackend, ]
    filter_class = StaffFilter


class StatusViewSet(viewsets.ModelViewSet):
    """Вьюшки по примечаниям (На работе, командировка и т.д.)"""
    queryset = Status.objects.all()
    serializer_class = StatusSerializer