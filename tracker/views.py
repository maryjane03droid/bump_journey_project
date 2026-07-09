from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PregnancyProfile, HealthLog
from .serializers import PregnancyProfileSerializer, HealthLogSerializer
from staff.models import AuditTrail


class SuccessMessageViewSetMixin:
    create_success_message = 'Created successfully'
    update_success_message = 'Updated successfully'
    delete_success_message = 'Deleted successfully'

    def _wrap(self, response, message):
        if response.status_code in [200, 201, 204]:
            payload = {'message': message}
            if response.data is not None:
                payload['data'] = response.data
            return Response(payload, status=response.status_code)
        return response

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return self._wrap(response, 'Retrieved successfully')

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return self._wrap(response, 'Retrieved successfully')

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return self._wrap(response, self.create_success_message)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return self._wrap(response, self.update_success_message)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return self._wrap(response, self.update_success_message)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': self.delete_success_message}, status=status.HTTP_200_OK)


class PregnancyProfileViewSet(SuccessMessageViewSetMixin, viewsets.ModelViewSet):
    serializer_class = PregnancyProfileSerializer
    permission_classes = [IsAuthenticated]
    create_success_message = 'Profile created successfully'
    update_success_message = 'Profile updated successfully'

    def get_queryset(self):
        user = self.request.user
        if user.is_any_staff or user.role == 'ADMIN':
            return PregnancyProfile.objects.all()
        return PregnancyProfile.objects.filter(patient=user)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'PATIENT':
            serializer.save(patient=user)
            AuditTrail.objects.create(
                user=user, user_role=user.role,
                action='PROFILE_CREATED', patient=user,
                description='Patient created pregnancy profile'
            )
        else:
            patient_id = self.request.data.get('patient')
            serializer.save(patient_id=patient_id)


class HealthLogViewSet(SuccessMessageViewSetMixin, viewsets.ModelViewSet):
    serializer_class = HealthLogSerializer
    permission_classes = [IsAuthenticated]
    create_success_message = 'Vitals recorded successfully'
    update_success_message = 'Vitals updated successfully'
    delete_success_message = 'Vitals deleted successfully'

    def get_queryset(self):
        user = self.request.user
        if user.is_any_staff or user.role == 'ADMIN':
            return HealthLog.objects.all()
        return HealthLog.objects.filter(patient=user)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)
        AuditTrail.objects.create(
            user=self.request.user, user_role=self.request.user.role,
            action='VITALS_ADDED', patient=self.request.user,
            description='Patient recorded daily vitals'
        )

    def perform_update(self, serializer):
        serializer.save()
        AuditTrail.objects.create(
            user=self.request.user, user_role=self.request.user.role,
            action='VITALS_UPDATED', patient=self.request.user,
            description='Patient updated daily vitals'
        )

    def perform_destroy(self, instance):
        AuditTrail.objects.create(
            user=self.request.user, user_role=self.request.user.role,
            action='VITALS_DELETED', patient=self.request.user,
            description='Patient deleted daily vitals'
        )
        instance.delete()