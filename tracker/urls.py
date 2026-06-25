from django.urls import path
from .views import VitalLogView, VitalLogDetailView, SymptomLogView, SymptomLogDetailView, ClinicalNoteDetailView

urlpatterns = [
    path('tracker/logs/', VitalLogView.as_view(), name='vital_logs'),
    path('tracker/logs/<int:pk>/', VitalLogDetailView.as_view(), name='vital_log_detail'),
    path('tracker/symptoms/', SymptomLogView.as_view(), name='symptom_logs'),
    path('tracker/symptoms/<int:pk>/', SymptomLogDetailView.as_view(), name='symptom_log_detail'),
    path('tracker/notes/<int:pk>/', ClinicalNoteDetailView.as_view(), name='clinical_note_detail'),
]