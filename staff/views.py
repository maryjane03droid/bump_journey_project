from rest_framework import viewsets, permissions
from .models import Appointment, ClinicalNote
from .serializers import AppointmentSerializer, ClinicalNoteSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Appointment.objects.all()
        elif user.role == 'STAFF':
            return Appointment.objects.filter(doctor=user)
        return Appointment.objects.filter(patient=user)


class ClinicalNoteViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicalNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['STAFF', 'ADMIN']:
            return ClinicalNote.objects.all()
        return ClinicalNote.objects.filter(appointment__patient=user)