from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from qranalizer.models import QRCodeReading

class RankingViewTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpassword')
        self.user2 = User.objects.create_user(username='user2', password='testpassword')

        QRCodeReading.objects.create(user=self.user1)
        QRCodeReading.objects.create(user=self.user2)

        # Obtenha o token para autenticação
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'user1', 'password': 'testpassword'})
        self.token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_ranking_view(self):
        response = self.client.get(reverse('ranking'))
        print("Response status code:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['username'], 'user1')
        self.assertEqual(response.data[0]['points'], 1)
        self.assertEqual(response.data[1]['username'], 'user2')
        self.assertEqual(response.data[1]['points'], 1)

    def test_ranking_view_without_authentication(self):
        # Remove o token de autenticação
        self.client.credentials()
        response = self.client.get(reverse('ranking'))
        print("Response status code:", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
