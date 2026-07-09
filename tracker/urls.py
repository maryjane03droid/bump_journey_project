from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PregnancyProfileViewSet, HealthLogViewSet

router = DefaultRouter()
router.register(r'pregnancy-profiles', PregnancyProfileViewSet, basename='pregnancy-profile')
router.register(r'health-logs', HealthLogViewSet, basename='health-log')

urlpatterns = [
    path('', include(router.urls)),
]
