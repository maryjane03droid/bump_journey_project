from rest_framework import viewsets, permissions, exceptions
from .models import PregnancyProfile, HealthLog
from .serializers import PregnancyProfileSerializer, HealthLogSerializer

class PregnancyProfileViewSet(viewsets.ModelViewSet):
    serializer_class = PregnancyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['STAFF', 'ADMIN']:
            return PregnancyProfile.objects.all().select_related('patient')
        return PregnancyProfile.objects.filter(patient=user)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role in ['STAFF', 'ADMIN']:
            if 'patient' not in self.request.data:
                raise exceptions.ValidationError({"patient": "Medical staff must explicitly provide a patient ID."})
            serializer.save()
        else:
            serializer.save(patient=user)


class HealthLogViewSet(viewsets.ModelViewSet):
    serializer_class = HealthLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['STAFF', 'ADMIN']:
            return HealthLog.objects.all().select_related('patient')
        return HealthLog.objects.filter(patient=user)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role in ['STAFF', 'ADMIN']:
            if 'patient' not in self.request.data:
                raise exceptions.ValidationError({"patient": "Medical staff must explicitly provide a patient ID."})
            serializer.save()
        else:
            serializer.save(patient=user)