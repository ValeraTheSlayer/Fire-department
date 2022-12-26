from django.contrib import admin
from .models import *

admin.site.register(UserInfo)
#admin.site.register(City)
admin.site.register(BorderPost)
admin.site.register(QuestionCategory)
# admin.site.register(ResponsiblePerson)
admin.site.register(CurrentAppeal)
admin.site.register(ApiData)
admin.site.register(StatisticCallNumber)
admin.site.register(StatisticQuestionCategory)
admin.site.register(EmergencyRank)
admin.site.register(EmergencyType)
admin.site.register(ObjectCategory)
# admin.site.register(Position)
# class PositionAdmin(admin.ModelAdmin):
#     list_display = ('name', 'main_position', 'order_number')
#     list_display_links = ('name',)
#     list_filter = ('name', 'main_position', 'order_number')
#
#
# admin.site.register(Position, PositionAdmin)
#

# # admin.site.register(Staff)
# class StaffAdmin(admin.ModelAdmin):
#     list_display = ('department', 'full_name', 'position', 'status', 'get_city')
#     list_display_links = ('department', 'full_name')
#     search_fields = ['full_name']
#     list_filter = ('department', 'position', 'status', 'gdzs')
#
#     def get_city(self, obj):
#         return obj.department.city
#
#     get_city.short_description = 'Город'
#     get_city.admin_order_field = 'department__city'
#
#
# admin.site.register(Staff, StaffAdmin)
