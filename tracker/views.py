# In your views.py
from rest_framework import viewsets, permissions
from .models import PregnancyProfile, HealthLog
from .serializers import PregnancyProfileSerializer, HealthLogSerializer

class PregnancyProfileViewSet(viewsets.ModelViewSet):
    serializer_class = PregnancyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return PregnancyProfile.objects.all()
        return PregnancyProfile.objects.filter(patient=user)

class HealthLogViewSet(viewsets.ModelViewSet):
    serializer_class = HealthLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Doctors see all logs (so they can monitor the dashboard)
        if user.is_staff or user.is_superuser:
            return HealthLog.objects.all().order_by('-recorded_at')
        # Patients only see their own daily logs
        return HealthLog.objects.filter(patient=user).order_by('-recorded_at')

    def perform_create(self, serializer):
        # Automatically attach the logged-in patient when they submit a daily log
        serializer.save(patient=self.request.user)