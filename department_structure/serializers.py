from rest_framework import serializers

from .models import FireDepartment
from transport.serializers import TransportSerializer


class FireDepartmentSerializer(serializers.ModelSerializer):
    """Сериализатор для видов информации"""
    transport_set = TransportSerializer(many=True)

    class Meta:
        model = FireDepartment
        fields = "__all__"