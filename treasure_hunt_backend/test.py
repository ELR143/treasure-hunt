from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('get-treasures')
        data = {'name': 'test_treasure','latitude': 1,'longitude':0}
        response = self.client.post( url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        