from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from .models import Appointment, StaffNote, AuditTrail
from .serializers import (
    AppointmentSerializer,
    StaffNoteSerializer,
    AuditTrailSerializer,
    UserSerializer
)

from accounts.permissions import IsAnyStaff

User = get_user_model()


class SuccessMessageViewSetMixin:

    create_success_message = 'Created successfully'
    update_success_message = 'Updated successfully'
    delete_success_message = 'Deleted successfully'

    def _wrap(self, response, message):
        if response.status_code in [200, 201, 204]:
            payload = {
                'message': message
            }

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

        return Response(
            {'message': self.delete_success_message},
            status=status.HTTP_200_OK
        )


class AppointmentViewSet(
    SuccessMessageViewSetMixin,
    viewsets.ModelViewSet
):

    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    create_success_message = (
        'Appointment requested successfully. Awaiting staff confirmation.'
    )

    def get_queryset(self):

        user = self.request.user

        if user.role == 'PATIENT':
            return Appointment.objects.filter(
                patient=user
            )

        if user.is_specialist_staff:
            return Appointment.objects.filter(
                referred_to=user
            )

        if user.is_primary_staff or user.role == 'ADMIN':
            return Appointment.objects.all()

        return Appointment.objects.none()


    def perform_create(self, serializer):

        user = self.request.user

        if user.role == 'PATIENT':

            serializer.save(
                patient=user,
                status='REQUESTED'
            )

            AuditTrail.objects.create(
                user=user,
                user_role=user.role,
                action='APPOINTMENT_REQUESTED',
                patient=user,
                description=(
                    f'Patient requested appointment: '
                    f'{serializer.instance.reason}'
                )
            )

        else:

            patient_id = self.request.data.get('patient')

            serializer.save(
                doctor=user,
                patient_id=patient_id,
                status='SCHEDULED'
            )


    def partial_update(self, request, *args, **kwargs):

        appointment = self.get_object()
        new_status = request.data.get('status')

        if new_status:

            appointment.status = new_status
            appointment.save()

            AuditTrail.objects.create(
                user=request.user,
                user_role=request.user.role,
                action='APPOINTMENT_COMPLETED'
                if new_status == 'COMPLETED'
                else 'CASE_LOCKED',
                patient=appointment.patient,
                description=(
                    f'Appointment status changed to {new_status}'
                )
            )

            return Response(
                {
                    "message": "Appointment updated successfully",
                    "data": AppointmentSerializer(appointment).data
                },
                status=status.HTTP_200_OK
            )

        return super().partial_update(
            request,
            *args,
            **kwargs
        )


class ReferAppointmentView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAnyStaff
    ]

    def post(self, request, pk):

        try:
            appointment = Appointment.objects.get(pk=pk)

        except Appointment.DoesNotExist:

            return Response(
                {
                    'message':'Appointment not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        referred_to_id = request.data.get(
            'referred_to'
        )

        if not referred_to_id:

            return Response(
                {
                    'message':'referred_to field is required'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            referred_to_user = User.objects.get(
                id=referred_to_id,
                role__in=[
                    'DOCTOR',
                    'PEDIATRICIAN',
                    'NURSE',
                    'MIDWIFE',
                    'NUTRITIONIST',
                    'LAB_TECHNICIAN',
                    'THERAPIST'
                ]
            )

        except User.DoesNotExist:

            return Response(
                {
                    'message':'Staff member not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        appointment.referred_by = request.user
        appointment.referred_to = referred_to_user
        appointment.is_locked = False
        appointment.locked_by = None

        role_status_map = {
            'DOCTOR': 'NEEDS_DOCTOR_ATTENTION',
            'PEDIATRICIAN': 'NEEDS_DOCTOR_ATTENTION',
            'MIDWIFE': 'NEEDS_MIDWIFE_ATTENTION',
            'NUTRITIONIST': 'NEEDS_NUTRITIONIST_ATTENTION',
            'LAB_TECHNICIAN': 'NEEDS_LAB_ATTENTION',
            'THERAPIST': 'NEEDS_THERAPIST_ATTENTION',
            'NURSE': 'NEEDS_DOCTOR_ATTENTION'
        }

        appointment.status = role_status_map.get(
            referred_to_user.role,
            'REFERRED'
        )

        appointment.save()

        AuditTrail.objects.create(
            user=request.user,
            user_role=request.user.role,
            action='CASE_REFERRED',
            patient=appointment.patient,
            description=(
                f'Referred to {referred_to_user.username}'
            )
        )

        return Response(
            {
                'message':
                f'Appointment referred to {referred_to_user.username} successfully.'
            },
            status=status.HTTP_200_OK
        )


class LockAppointmentView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAnyStaff
    ]

    def post(self, request, pk):

        try:
            appointment = Appointment.objects.get(pk=pk)

        except Appointment.DoesNotExist:

            return Response(
                {
                    'message':'Appointment not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        appointment.is_locked = True
        appointment.locked_by = request.user
        appointment.doctor = request.user
        appointment.status = 'LOCKED'

        appointment.save()

        AuditTrail.objects.create(
            user=request.user,
            user_role=request.user.role,
            action='CASE_LOCKED',
            patient=appointment.patient,
            description=(
                f'Case locked by {request.user.username}'
            )
        )

        return Response(
            {
                'message':
                'Case locked successfully.'
            },
            status=status.HTTP_200_OK
        )


class StaffListView(generics.ListAPIView):

    permission_classes = [
        IsAuthenticated,
        IsAnyStaff
    ]

    serializer_class = UserSerializer

    def get_queryset(self):

        return User.objects.filter(
            role__in=[
                'DOCTOR',
                'PEDIATRICIAN',
                'NURSE',
                'MIDWIFE',
                'NUTRITIONIST',
                'LAB_TECHNICIAN',
                'THERAPIST'
            ],
            is_approved=True
        ).order_by(
            'username'
        )
        
    # Standardizing the API response structural wrapping
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                'message': 'Staff members retrieved successfully',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


class StaffNoteViewSet(
    SuccessMessageViewSetMixin,
    viewsets.ModelViewSet
):

    serializer_class = StaffNoteSerializer

    permission_classes = [
        IsAuthenticated,
        IsAnyStaff
    ]

    create_success_message = (
        'Note added successfully'
    )

    def get_queryset(self):
        return StaffNote.objects.all()

    def perform_create(self, serializer):

        serializer.save(
            author=self.request.user
        )

        AuditTrail.objects.create(
            user=self.request.user,
            user_role=self.request.user.role,
            action='NOTE_ADDED',
            patient=serializer.instance.patient,
            description='Staff note added'
        )


class AuditTrailListView(generics.ListAPIView):

    serializer_class = AuditTrailSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        user = self.request.user

        if user.role == 'PATIENT':

            return AuditTrail.objects.filter(
                patient=user
            )

        return AuditTrail.objects.all()


class StaffPatientListView(generics.ListAPIView):

    permission_classes = [
        IsAuthenticated,
        IsAnyStaff
    ]

    def get_queryset(self):

        return User.objects.filter(
            role='PATIENT'
        ).order_by(
            'username'
        )

    def list(self, request, *args, **kwargs):

        patients = self.get_queryset().values(
            'id',
            'username',
            'email'
        )

        return Response(
            {
                'message':
                'Patients retrieved successfully',

                'data':
                list(patients)
            },
            status=status.HTTP_200_OK
        )