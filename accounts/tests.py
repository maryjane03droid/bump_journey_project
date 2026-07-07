from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegisterEndpointTests(APITestCase):
    def test_register_returns_success_message(self):
        url = reverse('auth_register')
        data = {
            'username': 'newpatient',
            'email': 'newpatient@example.com',
            'password': 'StrongPass123!',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User registered successfully')
