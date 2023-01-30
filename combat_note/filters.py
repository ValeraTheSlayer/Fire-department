from django_filters import rest_framework as filters
from .models import LineNoteMan, LineNoteTrans


class LineNoteManFilter(filters.FilterSet):
    data_filter = filters.DateFilter(field_name='date_line_note', label='все записи за эту дату')

    class Meta:
        model = LineNoteMan
        fields = ['data_filter']


class LineNoteTransFilter(filters.FilterSet):
    data_filter = filters.DateFilter(field_name='date_line_note', label='все записи за эту дату')

    class Meta:
        model = LineNoteTrans
        fields = ['data_filter']