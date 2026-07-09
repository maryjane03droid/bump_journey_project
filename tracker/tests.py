
# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class HealthLogEndpointTests(APITestCase):
    def setUp(self):
        self.patient = User.objects.create_user(username='testpatient', password='password123', role='PATIENT')
        self.client.force_authenticate(user=self.patient)

    def test_patient_can_create_health_log_without_providing_patient_field(self):
        """Patient should not need to provide patient field—it's auto-filled from request user"""
        url = reverse('health-log-list')
        data = {
            'weight_kg': 75.5,
            'blood_pressure': '110/30',
            'fetal_kick_count': 12,
            'symptoms': 'Mild nausea',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['patient'], str(self.patient.id))
        self.assertEqual(response.data['data']['weight_kg'], 75.5)


class SymptomLogTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)

    def test_create_symptom_log(self):
        url = reverse('symptom-log-list') # Ensure you have this name in urls.py
        data = {'symptom_name': 'Nausea', 'intensity': 5}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)