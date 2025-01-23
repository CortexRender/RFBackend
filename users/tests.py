from rest_framework import status
from rest_framework.test import APITestCase

from .models import RFUser


class UserTests(APITestCase):
    def setUp(self):
        self.user = RFUser.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com',
            is_superuser=False
        )
        self.login_url = '/api/users/login/'
        self.register_url = '/api/users/register/'
        self.user_info_url = '/api/users/me/'

    def test_register_user(self):
        data = {
            "username": "newuser",
            "password": "newpassword123",
            "email": "newuser@example.com",
            "is_superuser": False,
            "render_coin": 0
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], "newuser")
        self.assertEqual(response.data['render_coin'], 0)

        self.assertTrue(RFUser.objects.filter(username="newuser").exists())

    def test_login_user(self):
        data = {
            "username": "testuser",
            "password": "password123"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_user_info(self):
        login_response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "password123"
        })
        access_token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "testuser")
        self.assertEqual(response.data['email'], "testuser@example.com")
        self.assertEqual(response.data['render_coin'], 0)

    def test_get_user_info_unauthorized(self):
        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
