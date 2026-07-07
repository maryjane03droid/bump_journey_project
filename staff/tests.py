from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AppointmentEndpointTests(APITestCase):
    def test_staff_can_create_appointment_for_patient_using_uuid(self):
        staff_user = User.objects.create_user(username='staff', password='password123', role='STAFF', is_staff=True)
        patient_user = User.objects.create_user(username='patient', password='password123', role='PATIENT')
        self.client.force_authenticate(user=staff_user)

        url = reverse('appointment-list')
        data = {
            'patient': str(patient_user.id),
            'date': '2026-01-15',
            'time': '10:30:00',
            'reason': 'Routine checkup',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['patient'], str(patient_user.id))
