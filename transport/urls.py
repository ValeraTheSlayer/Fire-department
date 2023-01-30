from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('transport', views.TransportViewSet)
router.register('transport_type', views.TransTypeViewSet)
router.register('transport_model', views.TransModelViewSet)
router.register('transport_brand', views.BrandViewSet)
router.register('transport_status', views.TransStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
