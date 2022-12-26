from .models import *
import django_filters


class CurrentAppealFilter(django_filters.FilterSet):
    date = django_filters.DateTimeFromToRangeFilter(field_name='date_of_call_start', label='Промежуток времени')

    class Meta:
        model = CurrentAppeal
        fields = ['date', 'status', 'question_category', 'income_call_number']

class ApiDataFilter(django_filters.FilterSet):
    date = django_filters.DateTimeFromToRangeFilter(field_name='start_time', label='Промежуток времени')

    class Meta:
        model = ApiData
        fields = ['date', 'number_in']
