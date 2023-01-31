from django.urls import path
from . import views

urlpatterns = [
    path('', views.test, name='map'),
    path('points_map', views.points_map, name='points_map'),
    path('new_point', views.new_point, name='point')
]