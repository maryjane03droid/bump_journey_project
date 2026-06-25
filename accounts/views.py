from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsAdminRole, IsStaffOrAdmin

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Invalid credentials provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = User.objects.get(username=request.data.get('username'))
        if (user.role in ['STAFF', 'ADMIN']) and not user.is_approved:
            return Response(
                {"detail": "Access Denied. Your account is pending Admin approval."},
                status=status.HTTP_403_FORBIDDEN
            )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class AdminUserManagementView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        users = User.objects.all().order_by('-id')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminUserDetailView(APIView):
    permission_classes = [IsAdminRole]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User record not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Allows promoting, demoting, or modifying approval status
        if 'role' in request.data:
            user.role = request.data['role']
        if 'is_approved' in request.data:
            user.is_approved = request.data['is_approved']
        
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            if user.is_superuser:
                return Response({"detail": "Root administrator accounts cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)
            user.delete()
            return Response({"detail": "User account successfully purged."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"detail": "User record not found."}, status=status.HTTP_404_NOT_FOUND)

class StaffPatientSearchView(APIView):
    permission_classes = [IsStaffOrAdmin]

    def get(self, request):
        patients = User.objects.filter(role='PATIENT').order_by('-id')
        search_query = request.query_params.get('search', None)
        if search_query:
            patients = patients.filter(username__icontains=search_query)
        serializer = UserSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PatientHistoryView(APIView):
    permission_classes = [IsStaffOrAdmin]

    def get(self, request, pk):
        try:
            patient = User.objects.get(pk=pk, role='PATIENT')
        except User.DoesNotExist:
            return Response({"detail": "Patient record not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Pull everything connected to this specific patient identity
        vitals = patient.vital_logs.all().values('id', 'weight', 'bp', 'created_at')
        symptoms = patient.symptom_logs.all().values('id', 'symptom_name', 'severity', 'notes', 'created_at')
        notes = patient.clinical_notes_received.all().values('id', 'notes', 'created_at', 'provider__username')
        
        payload = {
            "account": UserSerializer(patient).data,
            "medical_history": {
                "vitals": list(vitals),
                "symptoms": list(symptoms),
                "clinical_notes": list(notes)
            }
        }
        return Response(payload, status=status.HTTP_200_OK)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)