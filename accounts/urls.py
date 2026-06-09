from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, PatientProfileDetailView  # Added PatientProfileDetailView here

urlpatterns = [
    # 1. Registration Endpoint
    path('register/', RegisterView.as_view(), name='auth_register'),
    
    # 2. Login Endpoint (Returns access and refresh tokens automatically)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # 3. Token Refresh Endpoint
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 4. Profile Endpoint
    path('profile/', PatientProfileDetailView.as_view(), name='patient_profile'),
]