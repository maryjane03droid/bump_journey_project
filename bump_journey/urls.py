from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Standard, clean admin path without loops
    path('admin/', admin.site.urls),
    
    # App routers
    path('api/auth/', include('accounts.urls')),
    path('api/tracker/', include('tracker.urls')),
]