from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AppointmentEndpointTests(APITestCase):
    def setUp(self):
        self.patient = User.objects.create_user(username='patient', password='password123', role='PATIENT')
        self.staff_user = User.objects.create_user(username='staff', password='password123', role='STAFF', is_staff=True)

    def test_patient_can_request_appointment_with_pending_status(self):
        """Patient requests appointment without providing date/time—status should be REQUESTED"""
        self.client.force_authenticate(user=self.patient)

        url = reverse('appointment-list')
        data = {
            'reason': 'Routine Prenatal Checkup',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['status'], 'REQUESTED')
        self.assertEqual(response.data['data']['patient'], str(self.patient.id))
        self.assertIn('awaiting staff confirmation', response.data['message'].lower())

    def test_staff_can_schedule_appointment_directly(self):
        """Staff schedules appointment directly with all details—status should be SCHEDULED"""
        self.client.force_authenticate(user=self.staff_user)

        url = reverse('appointment-list')
        data = {
            'patient': str(self.patient.id),
            'date': '2026-01-15',
            'time': '10:30:00',
            'reason': 'Routine checkup',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['status'], 'SCHEDULED')
        self.assertEqual(response.data['data']['patient'], str(self.patient.id))
