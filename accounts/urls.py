from django.urls import path
from .views import (
    PatientRegisterView,
    StaffRegisterView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    AdminUserListView,
    AdminApproveStaffView,
    CareerApplicationCreateView,
    CareerApplicationListView,
    ContactMessageCreateView,
    ContactMessageListView,
)

urlpatterns = [
    # Auth
    path('register/', PatientRegisterView.as_view(), name='patient_register'),
    path('register/staff/', StaffRegisterView.as_view(), name='staff_register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    # Admin: user management
    path('admin/users/', AdminUserListView.as_view(), name='admin_user_list'),
    path('admin/users/<uuid:pk>/approve/', AdminApproveStaffView.as_view(), name='admin_approve_staff'),

    # Career applications
    path('careers/apply/', CareerApplicationCreateView.as_view(), name='career_apply'),
    path('admin/careers/', CareerApplicationListView.as_view(), name='career_list'),

    # Contact messages
    path('contact/', ContactMessageCreateView.as_view(), name='contact_create'),
    path('admin/messages/', ContactMessageListView.as_view(), name='contact_list'),
]