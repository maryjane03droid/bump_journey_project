import django_filters
from .models import PatientProfile

class PatientProfileFilter(django_filters.FilterSet):
    # Example: Filter profiles by an estimated due date range
    start_date = django_filters.DateFilter(field_name="estimated_due_date", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="estimated_due_date", lookup_expr='lte')

    class Meta:
        model = PatientProfile
        fields = ['estimated_due_date']