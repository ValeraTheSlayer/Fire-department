from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import FireDepartmentSerializer
from .models import FireDepartment
from transport.models import Transport
from transport.serializers import TransportSerializer


class FireDepartmentViewSet(viewsets.ModelViewSet):
    """Вьюшки по пожарной части (ПЧ). Здесь можно получить или создать новую пожарную часть."""
    queryset = FireDepartment.objects.all()
    serializer_class = FireDepartmentSerializer

    @action(methods=("GET", ), detail=True, url_path="transports")
    def getTransports(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = Transport.objects.filter(department=instance)
        serializer = TransportSerializer(instance, many=True)
        return Response(serializer.data)