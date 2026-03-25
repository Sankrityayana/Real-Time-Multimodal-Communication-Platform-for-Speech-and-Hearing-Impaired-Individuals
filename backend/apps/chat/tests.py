from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class ChatSessionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='chat@example.com',
            username='chat@example.com',
            password='StrongPass123!'
        )
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_session_and_list_messages(self):
        session_response = self.client.post('/api/chat/sessions/', {}, format='json')
        self.assertEqual(session_response.status_code, status.HTTP_201_CREATED)

        session_id = session_response.data['id']
        messages_response = self.client.get(f'/api/chat/sessions/{session_id}/messages/')
        self.assertEqual(messages_response.status_code, status.HTTP_200_OK)
        self.assertEqual(messages_response.data, [])
