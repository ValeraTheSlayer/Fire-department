from django_filters import rest_framework as filters
from .models import Staff

class StaffFilter(filters.FilterSet):
    position_name_start = filters.CharFilter(field_name='position__name', lookup_expr='istartswith', label='начало должности')
    position_name_end = filters.CharFilter(field_name='position__name', lookup_expr='iendswith', label='конец должности')

    class Meta:
        model = Staff
        fields = ['position_name_start', 'position_name_end']