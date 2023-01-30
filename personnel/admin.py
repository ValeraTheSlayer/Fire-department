from django.contrib import admin
from .models import Staff, Position, Status, Sentry
# Register your models here.
admin.site.register(Staff)
admin.site.register(Position)
admin.site.register(Status)
admin.site.register(Sentry)

