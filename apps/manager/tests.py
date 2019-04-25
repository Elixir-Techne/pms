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


class ManagerTests(APITestCase):
    fixtures = ['user_auth.json', 'test_master.json', 'test_employees.json', 'test_employment.json',
                'test_clients.json', 'test_manager.json']

    def test_create_manager(self):
        user = 2
        data = {
            'user': user,
            'gender': 'male',
            'first_name': 'sky',
            'last_name': 'patel',
            'ssn': '123456',
            'birth_date': '2018-03-03',
            'address1': '4/a dadsgard',
            'address2': '2da datgrffs',
            'country': 1,
            'state': 1,
            'city': 1,
            'zip_code': '38008',
            'phone': '1234567890',
            'status': 'pending'
        }

        with login(self.client, username='test1', password='akash@123'):
            url = reverse('managers:managers-list')
            response = self.client.post(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_managers(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('managers:managers-list')
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_managers(self):
        user = 1
        data = {
            'user': user,
            'gender': 'male',
            'first_name': 'sky',
            'last_name': 'patel',
            'ssn': '123456',
            'birth_date': '2018-03-03',
            'address1': '4/a dadsgard',
            'address2': '2da datgrffs',
            'country': 1,
            'state': 1,
            'city': 1,
            'zip_code': '38008',
            'phone': '1234567890',
            'status': 'approved'
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('managers:managers-detail', args=(1,))
            response = self.client.put(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_failed_update_managers(self):
        user = 10
        data = {
            'user': user,
            'gender': 'male',
            'first_name': 'sky',
            'last_name': 'patel',
            'ssn': '123456',
            'birth_date': '2018-03-03',
            'address1': '4/a dadsgard',
            'address2': '2da datgrffs',
            'country': 1,
            'state': 1,
            'city': 1,
            'zip_code': '38008',
            'phone': '1234567890',
            'status': 'approved'
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('managers:managers-detail', args=(3,))
            response = self.client.put(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_managers(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('managers:managers-detail', args=(1,))
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
