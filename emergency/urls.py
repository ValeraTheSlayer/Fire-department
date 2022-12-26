from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('current_emergency', views.CurrentEmergencyViewSet)
router.register('emergency_rank', views.EmergencyRankViewSet)
router.register('emergency_type', views.EmergencyTypeViewSet)
router.register('fire_category', views.ObjectCategoryViewSet)
router.register('default_event', views.DefaultEventViewSet)
router.register('journal_event', views.JournalEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
