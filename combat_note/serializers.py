from rest_framework import serializers

from .models import LineNoteMan, LineNoteTrans


class LineNoteManSerializer(serializers.ModelSerializer):
    """Сериализатор для строевой записки ЛС"""
    position_name = serializers.SlugField(source='position', read_only=True)
    staff_name = serializers.SlugField(source='staff', read_only=True)
    status_name = serializers.SlugField(source='status', read_only=True)

    class Meta:
        model = LineNoteMan
        fields = "__all__"


class LineNoteTransSerializer(serializers.ModelSerializer):
    """Сериализатор для строевой записки по техникам"""
    department_name = serializers.SlugField(source='department', read_only=True)
    transport_name = serializers.SlugField(source='transport', read_only=True)
    trans_status_name = serializers.SlugField(source='trans_status', read_only=True)

    class Meta:
        model = LineNoteTrans
        fields = "__all__"
