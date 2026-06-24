from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, StaffNoteViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'notes', StaffNoteViewSet, basename='staffnote')

urlpatterns = [
    path('', include(router.urls)),
]