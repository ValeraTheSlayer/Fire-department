from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('personnel_status', views.StatusViewSet)
router.register('personnel_position', views.PositionViewSet)
router.register('personnel_staff', views.StaffViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
