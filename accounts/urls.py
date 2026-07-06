from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, PatientProfileDetailView, CustomTokenObtainPairView  # <-- Swap token view for CustomTokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # <-- Point here
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', PatientProfileDetailView.as_view(), name='patient_profile'),
]