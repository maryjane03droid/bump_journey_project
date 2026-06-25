from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView, AdminUserManagementView, AdminUserDetailView,
    StaffPatientSearchView, PatientHistoryView, ProfileView
)

urlpatterns = [
    path('accounts/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('accounts/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/users/', AdminUserManagementView.as_view(), name='admin_users'),
    path('accounts/users/<int:pk>/', AdminUserDetailView.as_view(), name='admin_user_detail'),
    path('accounts/patients/', StaffPatientSearchView.as_view(), name='staff_patients'),
    path('accounts/patients/<int:pk>/history/', PatientHistoryView.as_view(), name='patient_history'),
    path('accounts/profile/', ProfileView.as_view(), name='user_profile'),
]