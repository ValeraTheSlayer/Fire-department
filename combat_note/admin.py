from django.contrib import admin
from .models import LineNoteMan, LineNoteTrans, StaticValues
# Register your models here.
admin.site.register(LineNoteMan)
admin.site.register(LineNoteTrans)
admin.site.register(StaticValues)
