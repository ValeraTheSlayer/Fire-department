from django.forms import ModelForm
#from .models import *
from transport.models import Transport
from application.models import *
#from emergency.models import CurrentEmergency


class JournalEventForm(ModelForm):
    class Meta:
        model = JournalEvent
        fields = ['event']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].widget.attrs.update({'class': 'form-control'})
#
# #
class CurrentEmergencyForm(ModelForm):
    class Meta:
        model = CurrentAppeal
        fields = ['date_of_call_start', 'date_of_call_end', 'income_call_number', 'income_call_name', 'address',  'object_category', 'object_owner',
                   'short_question','emergency_type', 'emergency_rank', 'department', 'responsible_department_person' , # 'first_info_burning', 'staff',
                   'transport', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_call_start'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_of_call_end'].widget.attrs.update({'class': 'form-control'})
        self.fields['income_call_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['income_call_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        #self.fields['house_kv'].widget.attrs.update({'class': 'form-control'})
        self.fields['object_category'].widget.attrs.update({'class': 'form-select'})
        self.fields['object_owner'].widget.attrs.update({'class': 'form-select'})
        self.fields['short_question'].widget.attrs.update({'class': 'form-select'})
        self.fields['emergency_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['emergency_rank'].widget.attrs.update({'class': 'form-select'})
        self.fields['department'].widget.attrs.update({'class': 'form-select'})
        self.fields['responsible_department_person'].widget.attrs.update({'class': 'form-select'})
        self.fields['responsible_department_person'].label = "Руководитель тушения пожара"
 
        #self.fields['first_info_burning'].widget.attrs.update({'class': 'form-control'})
        #self.fields['staff'].widget.attrs.update({'class': 'form-select'})
        self.fields['transport'].widget.attrs.update({'class': 'form-select'})


class TransportForm(ModelForm):
    class Meta:
        model = Transport
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].widget.attrs.update({'class': 'form-select'})
        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        self.fields['trans_model'].widget.attrs.update({'class': 'form-select'})
        self.fields['new_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['department'].widget.attrs.update({'class': 'form-select'})
