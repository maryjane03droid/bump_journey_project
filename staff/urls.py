from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AppointmentViewSet,
    StaffNoteViewSet,
    ReferAppointmentView,
    LockAppointmentView,
    AuditTrailListView,
    StaffPatientListView,
)

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'notes', StaffNoteViewSet, basename='staffnote')

urlpatterns = [
    path('', include(router.urls)),
    path('appointments/<int:pk>/refer/', ReferAppointmentView.as_view(), name='appointment_refer'),
    path('appointments/<int:pk>/lock/', LockAppointmentView.as_view(), name='appointment_lock'),
    path('audit-trail/', AuditTrailListView.as_view(), name='audit_trail'),
    path('patients/', StaffPatientListView.as_view(), name='staff_patient_list'),
]