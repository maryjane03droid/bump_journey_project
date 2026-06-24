from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClinicalNoteViewSet

router = DefaultRouter()
router.register(r'notes', ClinicalNoteViewSet, basename='clinical-note')

urlpatterns = [
    path('', include(router.urls)),
]