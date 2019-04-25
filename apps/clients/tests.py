from contextlib import contextmanager

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


@contextmanager
def login(client, username='test1', password='test1@password'):
    url = reverse('rest_login')
    response = client.post(url, {
        'username': username, 'password': password}, format='json')
    # print(response.__dict__)
    token = response.data['token']
    # print(token)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    yield
    client.credentials()


class ClientTests(APITestCase):
    fixtures = ['user_auth.json', 'test_master.json', 'test_employees.json', 'test_employment.json',
                'test_clients.json']

    def test_create_client(self):
        user = 2
        data = {
            "name": "sky",
            "user": user,
            "trade": "pms test",
            "description": "testing",
            "email": "mangroliya.akash@gmail.com",
            "address": "ahmedabad",
            "contact_first_name": "sky",
            "contact_last_name": "patel",
            "phone": "9898222623",
            "status": "pending"
        }

        with login(self.client, username='test1', password='akash@123'):
            url = reverse('clients:clients-list')
            response = self.client.post(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_failed_create_client(self):
        user = 3
        data = {
            "name": "sky",
            "user": user,
            "trade": "pms test",
            "description": "testing",
            "email": "mangroliya.akash@gmail.com",
            "address": "ahmedabad",
            "contact_first_name": "sky",
            "contact_last_name": "patel",
            "phone": "9898222623",
            "status": "pending"
        }

        with login(self.client, username='test1', password='akash@123'):
            url = reverse('clients:clients-list')
            response = self.client.post(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_client(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('clients:clients-list')
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_client(self):
        user = 2
        data = {
            "name": "sky",
            "user": user,
            "trade": "pms test",
            "description": "testing",
            "email": "mangroliya.akash@gmail.com",
            "address": "ahmedabad",
            "contact_first_name": "sky",
            "contact_last_name": "patel",
            "phone": "9898222623",
            "status": "pending"
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('clients:clients-detail', args=(1,))
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_failed_update_client(self):
        data = {
            "name": "sky",
            "trade": "pms test",
            "description": "testing",
            "email": "mangroliya.akash@gmail.com",
            "address": "ahmedabad",
            "contact_first_name": "sky",
            "contact_last_name": "patel",
            "phone": "9898222623",
            "status": "pending"
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('clients:clients-detail', args=(1,))
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_client(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('clients:clients-detail', args=(1,))
            response = self.client.delete(url)
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
