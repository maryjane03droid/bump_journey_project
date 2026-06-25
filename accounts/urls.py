from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, ApproveStaffView

urlpatterns = [
    path('accounts/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('accounts/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/users/<int:pk>/approve/', ApproveStaffView.as_view(), name='approve_staff'),
]