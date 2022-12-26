from django_filters import rest_framework as dj_filters
#from .models import EmergencyType
from application.models import CurrentAppeal

# class BookmarkFilter(dj_filters.FilterSet):
#     name_st = dj_filters.CharFilter(field_name='name', lookup_expr='istartswith')

#     class Meta:
#         model = EmergencyType
#         fields = ['id', 'name', 'name_st']


class CurrentEmergencyFilter(dj_filters.FilterSet):
    created_date = dj_filters.DateFilter(field_name='date_of_call_start', lookup_expr='contains', label='Дата заявки')

    class Meta:
        model = CurrentAppeal
        fields = ['created_date']