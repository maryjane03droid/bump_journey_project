from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import RegisterSerializer, PatientProfileSerializer, CustomTokenObtainPairSerializer
from .models import PatientProfile

User = get_user_model()


class SuccessMessageMixin:
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


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            payload = {'message': 'Login successful', 'data': response.data}
            return Response(payload, status=status.HTTP_200_OK)
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            payload = {'message': 'Token refreshed successfully', 'data': response.data}
            return Response(payload, status=status.HTTP_200_OK)
        return response


class RegisterView(SuccessMessageMixin, generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    create_success_message = 'User registered successfully'


class PatientProfileDetailView(SuccessMessageMixin, generics.RetrieveUpdateAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]
    update_success_message = 'Profile updated successfully'

    def get_object(self):
        profile, created = PatientProfile.objects.get_or_create(user=self.request.user)
        return profile