from rest_framework import viewsets
from .serializers import TransportSerializer, TransTypeSerializer, TransModelSerializer, BrandSerializer, \
    TransStatusSerializer

from .models import Transport, TransType, Brand, Model, TransStatus


class TransportViewSet(viewsets.ModelViewSet):
    """Вьюшки для транспортов."""
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer


class TransTypeViewSet(viewsets.ModelViewSet):
    """Вьюшки по типам транспортов."""
    queryset = TransType.objects.all()
    serializer_class = TransTypeSerializer


class TransModelViewSet(viewsets.ModelViewSet):
    """Вьюшки по моделям транспортов."""
    queryset = Model.objects.all()
    serializer_class = TransModelSerializer


class BrandViewSet(viewsets.ModelViewSet):
    """Вьюшки по марке (brand) транспортов."""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class TransStatusViewSet(viewsets.ModelViewSet):
    """Вьюшки о состоянии транспортов."""
    queryset = TransStatus.objects.all()
    serializer_class = TransStatusSerializer