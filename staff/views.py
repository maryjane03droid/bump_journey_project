from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Appointment, StaffNote
from .serializers import AppointmentSerializer, StaffNoteSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    # You need this to auto-assign the doctor!
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)


class StaffNoteViewSet(viewsets.ModelViewSet):
    queryset = StaffNote.objects.all()
    serializer_class = StaffNoteSerializer
    permission_classes = [IsAuthenticated]

    # You need this to auto-assign the author!
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)