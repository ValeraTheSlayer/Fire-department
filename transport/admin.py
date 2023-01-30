from django.contrib import admin
from .models import Transport, Brand, Model, TransType, TransStatus
# Register your models here.
admin.site.register(Transport)
admin.site.register(Brand)
admin.site.register(Model)
admin.site.register(TransType)
admin.site.register(TransStatus)
