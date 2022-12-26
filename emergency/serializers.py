from rest_framework import serializers

from .models import ObjectCategory, EmergencyRank, EmergencyType, CurrentEmergency, DefaultEvent, JournalEvent


class ObjectCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории пожаров"""

    class Meta:
        model = ObjectCategory
        fields = "__all__"


class EmergencyRankSerializer(serializers.ModelSerializer):
    """Сериализатор для ранга происшествия"""

    class Meta:
        model = EmergencyRank
        fields = "__all__"


class EmergencyTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для типа происшествия"""

    class Meta:
        model = EmergencyType
        fields = "__all__"


class JournalEventSerializer(serializers.ModelSerializer):
    """Сериализатор для журнала событий"""
    emergency_name = serializers.SlugField(source='emergency', read_only=True)

    class Meta:
        model = JournalEvent
        fields = "__all__"


class CurrentEmergencySerializer(serializers.ModelSerializer):
    """Сериализатор для заявок"""
    user_created_event_name = serializers.SlugField(source='user_created_event', read_only=True)
    object_category_name = serializers.SlugField(source='object_category', read_only=True)
    emergency_type_name = serializers.SlugField(source='emergency_type', read_only=True)
    emergency_rank_name = serializers.SlugField(source='emergency_rank', read_only=True)
    department_name = serializers.StringRelatedField(source='department', read_only=True, many=True)
    transport_name = serializers.StringRelatedField(source='transport', read_only=True, many=True)
    staff_name = serializers.SlugField(source='staff', read_only=True)

    class Meta:
        model = CurrentEmergency
        fields = "__all__"


class DefaultEventSerializer(serializers.ModelSerializer):
    """Сериализатор для частых событий"""

    class Meta:
        model = DefaultEvent
        fields = "__all__"