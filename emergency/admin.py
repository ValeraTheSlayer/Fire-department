from django.contrib import admin
from .models import CurrentEmergency, JournalEvent, EmergencyRank, EmergencyType, ObjectCategory

# Register your models here.
admin.site.register(CurrentEmergency)
admin.site.register(JournalEvent)
admin.site.register(EmergencyRank)
admin.site.register(EmergencyType)
admin.site.register(ObjectCategory)
 
