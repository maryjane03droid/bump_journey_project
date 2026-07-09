# In your views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import PregnancyProfile, HealthLog
from .serializers import PregnancyProfileSerializer, HealthLogSerializer


class SuccessMessageViewSetMixin:
    create_success_message = 'Created successfully'
    update_success_message = 'Updated successfully'
    delete_success_message = 'Deleted successfully'

    def _wrap_success_response(self, response, message):
        if response.status_code in [200, 201, 204]:
            payload = {'message': message}
            if response.data is not None:
                payload['data'] = response.data
            return Response(payload, status=response.status_code, headers=getattr(response, 'headers', {}))
        return response

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return self._wrap_success_response(response, 'Retrieved successfully')

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return self._wrap_success_response(response, 'Retrieved successfully')

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return self._wrap_success_response(response, self.create_success_message)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return self._wrap_success_response(response, self.update_success_message)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return self._wrap_success_response(response, self.update_success_message)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            return Response({'message': self.delete_success_message}, status=status.HTTP_200_OK)
        return response


class PregnancyProfileViewSet(SuccessMessageViewSetMixin, viewsets.ModelViewSet):
    serializer_class = PregnancyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return PregnancyProfile.objects.all()
        return PregnancyProfile.objects.filter(patient=user)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'PATIENT':
            serializer.save(patient=user)
        else:
            patient_id = self.request.data.get('patient')
            serializer.save(patient_id=patient_id)


class HealthLogViewSet(SuccessMessageViewSetMixin, viewsets.ModelViewSet):
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