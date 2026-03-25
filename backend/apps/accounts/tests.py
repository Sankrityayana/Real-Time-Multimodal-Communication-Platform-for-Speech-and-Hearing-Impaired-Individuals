from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthTests(APITestCase):
    def test_register_and_login(self):
        register_payload = {
            'email': 'test@example.com',
            'password': 'StrongPass123!',
            'name': 'Test User'
        }
        register_response = self.client.post('/api/auth/register/', register_payload, format='json')
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        login_response = self.client.post(
            '/api/auth/login/',
            {'email': register_payload['email'], 'password': register_payload['password']},
            format='json'
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)
        self.assertIn('refresh', login_response.data)
