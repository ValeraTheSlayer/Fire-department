from django.urls import path
from . import views

urlpatterns = [
    path('', views.test, name='map'),
    path('aj', views.test, name='aj'),
]