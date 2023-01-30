from rest_framework import serializers

from .models import Position, Staff, Status

class PositionSerializer(serializers.ModelSerializer):
    """Сериализатор для должностей"""

    class Meta:
        model = Position
        fields = "__all__"


class StaffSerializer(serializers.ModelSerializer):
    """Сериализатор для сотрудников"""
    position_name = serializers.SlugField(source='position', read_only=True)
    department_name = serializers.SlugField(source='department', read_only=True)
    status_name = serializers.SlugField(source='status', read_only=True)

    class Meta:
        model = Staff
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    """Сериализатор для примечаний ЛС"""

    class Meta:
        model = Status
        fields = "__all__"