from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

# Custom JWT Login to enforce Admin approval for Staff/Admin roles
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = User.objects.get(username=request.data.get('username'))
        
        if not user.is_approved:
            return Response(
                {"detail": "Your staff account is pending Admin approval."}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

# Admin-only view to approve pending accounts
class ApproveStaffView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        # Enforce that only users with the ADMIN role can access this endpoint
        if request.user.role != 'ADMIN':
            return Response({"detail": "Permission denied. Admins only."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user_to_approve = User.objects.get(pk=pk)
            user_to_approve.is_approved = True
            user_to_approve.save()
            return Response(
                {"detail": f"User {user_to_approve.username} has been successfully approved."}, 
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)