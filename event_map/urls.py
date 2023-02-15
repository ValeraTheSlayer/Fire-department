from django.urls import path
from . import views

urlpatterns = [
    path('points_map', views.points_map, name='points_map'),
    path('new_point', views.new_point, name='point'),
    path('history_points', views.history_points, name='history_points'),
    path('get_polygon_1_points', views.get_polygon_1_points, name='get_polygon_1_points'),
    path('get_polygon_2_points', views.get_polygon_2_points, name='get_polygon_2_points'),
    path('get_polygon_3_points', views.get_polygon_3_points, name='get_polygon_3_points'),
    path('get_polygon_4_points', views.get_polygon_4_points, name='get_polygon_4_points'),
    path('get_department', views.get_department, name='get_department')
]