
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import SymptomLog
from .serializers import SymptomLogSerializer

class SymptomLogListCreateView(generics.ListCreateAPIView):
    serializer_class = SymptomLogSerializer
    permission_classes = [IsAuthenticated]  # Guarded by JWT tokens

    def get_queryset(self):
        # Securely filters the records so a patient ONLY sees their own logs
        return SymptomLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically attaches the logged-in user context to the new database row
        serializer.save(user=self.request.user)