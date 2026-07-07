from django.urls import path
from .views import RegisterView, PatientProfileDetailView, CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', PatientProfileDetailView.as_view(), name='patient_profile'),
]