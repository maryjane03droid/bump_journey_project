
# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class SymptomLogTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)

    def test_create_symptom_log(self):
        url = reverse('symptom-log-list') # Ensure you have this name in urls.py
        data = {'symptom_name': 'Nausea', 'intensity': 5}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)