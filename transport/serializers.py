from rest_framework import serializers

from .models import Transport, TransType, Brand, Model, TransStatus


class TransTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для видов информации"""

    class Meta:
        model = TransType
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):
    """Сериализатор для видов информации"""

    class Meta:
        model = Brand
        fields = "__all__"

class TransModelSerializer(serializers.ModelSerializer):
    """Сериализатор для видов информации"""

    class Meta:
        model = Model
        fields = "__all__"

class TransStatusSerializer(serializers.ModelSerializer):
    """Сериализатор для видов информации"""

    class Meta:
        model = TransStatus
        fields = "__all__"

class TransportSerializer(serializers.ModelSerializer):
    """Сериализатор для видов информации"""

    brand_name = serializers.SlugField(source='brand', read_only=True)
    type_name = serializers.SlugField(source='type', read_only=True)
    trans_model_name = serializers.SlugField(source='trans_model', read_only=True)
    department_name = serializers.SlugField(source='department', read_only=True)

    class Meta:
        model = Transport
        fields = "__all__"