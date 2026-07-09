from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import (
    PatientRegisterSerializer,
    StaffRegisterSerializer,
    CustomTokenObtainPairSerializer,
    UserSerializer,
    AdminApproveSerializer,
    CareerApplicationSerializer,
    ContactMessageSerializer,
)
from .models import CareerApplication, ContactMessage
from .permissions import IsAdminRole

User = get_user_model()


class SuccessMessageMixin:
    create_success_message = 'Created successfully'
    update_success_message = 'Updated successfully'

    def _wrap(self, response, message):
        if response.status_code in [200, 201]:
            return Response(
                {'message': message, 'data': response.data},
                status=response.status_code
            )
        return response


# ─── Auth ─────────────────────────────────────────────

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response(
                {'message': 'Login successful', 'data': response.data},
                status=status.HTTP_200_OK
            )
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response(
                {'message': 'Token refreshed successfully', 'data': response.data},
                status=status.HTTP_200_OK
            )
        return response


# ─── Registration ─────────────────────────────────────

class PatientRegisterView(SuccessMessageMixin, generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PatientRegisterSerializer
    create_success_message = 'Patient registered successfully'

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return self._wrap(response, self.create_success_message)


class StaffRegisterView(SuccessMessageMixin, generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = StaffRegisterSerializer
    create_success_message = 'Staff registered successfully. Admin will approve within 24 hours.'

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return self._wrap(response, self.create_success_message)


# ─── Admin: User Management ──────────────────────────

class AdminUserListView(generics.ListAPIView):
    """Admin sees all users, filterable by role via ?role=DOCTOR"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(role=role.upper())
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {'message': 'Users retrieved successfully', 'data': response.data},
            status=status.HTTP_200_OK
        )


class AdminApproveStaffView(generics.UpdateAPIView):
    """Admin approves or rejects staff by setting is_approved."""
    queryset = User.objects.all()
    serializer_class = AdminApproveSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        user = self.get_object()
        msg = f'{user.username} has been approved.' if user.is_approved else f'{user.username} has been rejected.'
        return Response(
            {'message': msg, 'data': response.data},
            status=status.HTTP_200_OK
        )


# ─── Career Applications ─────────────────────────────

class CareerApplicationCreateView(generics.CreateAPIView):
    """Public: anyone can submit a career application."""
    queryset = CareerApplication.objects.all()
    serializer_class = CareerApplicationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            return Response(
                {'message': 'Application submitted successfully. We will review and get back to you.', 'data': response.data},
                status=status.HTTP_201_CREATED
            )
        return response


class CareerApplicationListView(generics.ListAPIView):
    """Admin views all career applications, filterable by ?status=PENDING"""
    serializer_class = CareerApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_queryset(self):
        queryset = CareerApplication.objects.all()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter.upper())
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {'message': 'Applications retrieved successfully', 'data': response.data},
            status=status.HTTP_200_OK
        )


# ─── Contact Messages ────────────────────────────────

class ContactMessageCreateView(generics.CreateAPIView):
    """Public: anyone can send a message to the admin."""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            return Response(
                {'message': 'Message sent successfully. We will get back to you shortly.', 'data': response.data},
                status=status.HTTP_201_CREATED
            )
        return response


class ContactMessageListView(generics.ListAPIView):
    """Admin views all contact messages."""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {'message': 'Messages retrieved successfully', 'data': response.data},
            status=status.HTTP_200_OK
        )