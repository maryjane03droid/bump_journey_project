from django.urls import path
from .views import SymptomLogListCreateView

urlpatterns = [
    path('symptoms/', SymptomLogListCreateView.as_view(), name='symptom_list_create'),
]