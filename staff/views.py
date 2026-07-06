from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Appointment, StaffNote
from .serializers import AppointmentSerializer, StaffNoteSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'PATIENT':
            serializer.save(patient=user)
        else:
            patient_id = self.request.data.get('patient')
            serializer.save(doctor=user, patient_id=patient_id)

class StaffNoteViewSet(viewsets.ModelViewSet):
    queryset = StaffNote.objects.all()
    serializer_class = StaffNoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)