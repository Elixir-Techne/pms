from contextlib import contextmanager

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


@contextmanager
def login(client, username='test1', password='test1@password'):
    url = reverse('rest_login')
    response = client.post(url, {'username': username, 'password': password}, format='json')
    token = response.data['token']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    yield
    client.credentials()


class ProjectTests(APITestCase):
    fixtures = ['user_auth.json', 'test_master.json', 'test_employees.json', 'test_employment.json',
                'test_clients.json', 'test_manager.json', 'test_project.json']

    def test_create_project(self):
        data = {
            "name": "customer sky",
            "description": "customer testing.",
            "customer": "1",
            "billing_method": "fixed_cost",
            "estimation": "10",
            "start_date": "2018-03-03",
            "end_date": "2019-03-03"
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:projects-list')
            response = self.client.post(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_failed_create_project_without_customer(self):
        data = {
            "name": "sky",
            "description": "sky testing.",
            "billing_method": "fixed_cost",
            "estimation": "25",
            "start_date": "2017-03-03",
            "end_date": "2018-03-03"
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:projects-list')
            response = self.client.post(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failed_create_project(self):
        data = {
            "name": "customer sky",
            "description": "customer testing.",
            "billing_method": "fixed_cost",
            "estimation": "10",
            "start_date": "2018-03-03",
            "end_date": "2019-03-03"
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:projects-list')
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_projects(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:projects-list')
            response = self.client.get(url)
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_project(self):
        data = {
            "name": "project1",
            "description": "project1 testing.",
            "billing_method": "fixed_cost",
            "customer": 1,
            "estimation": "15",
            "start_date": "2018-03-03",
            "end_date": "2020-03-03"
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:projects-detail', args=(1,))
            response = self.client.put(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_failed_update_project(self):
        data = {
            "name": "test",
            "description": "test project",
            "billing_method": "fixed_cost",
            "estimation": "15",
            "customer": 1,
            "start_date": "2018-03-03",
            "end_date": "2020-03-03"
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:projects-detail', args=(2,))
            response = self.client.put(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_failed_update_project_without_customer(self):
        data = {
            "name": "test",
            "description": "test project",
            "billing_method": "fixed_cost",
            "estimation": "15",
            "start_date": "2018-03-03",
            "end_date": "2020-03-03"
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:projects-detail', args=(1,))
            response = self.client.put(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_project(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:projects-detail', args=(1,))
            response = self.client.delete(url)
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CustomerTests(APITestCase):
    fixtures = ['user_auth.json', 'test_master.json', 'test_employees.json', 'test_employment.json',
                'test_clients.json', 'test_manager.json', 'test_project.json']

    def test_create_customer(self):
        data = {
            "client": 1,
            "first_name": "customer firstname",
            "last_name": "customer lastname",
            "email": "customer1@nomail.com",
            "phone": "1854788865",
            "country": 1,
            "state": 1,
            "city": 1,
            "zip_code": "380008",
        }

        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:customers-list')
            response = self.client.post(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_failed_create_customer(self):
        data = {
            "first_name": "customer firstname",
            "last_name": "customer lastname",
            "email": "customer1@nomail.com",
            "phone": "1854788865",
            "country": 1,
            "state": 1,
            "city": 1,
            "zip_code": "380008",
        }

        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:customers-list')
            response = self.client.post(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_customers(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:customers-list')
            response = self.client.get(url)
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_customer(self):
        data = {
            "client": 1,
            "first_name": "customer firstname",
            "last_name": "customer lastname",
            "email": "update.customer@nomail.com",
            "phone": "1854788865",
            "country": 1,
            "state": 1,
            "city": 1,
            "zip_code": "380008",
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:customers-detail', args=(1,))
            response = self.client.put(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_failed_update_customer(self):
        data = {
            "first_name": "customer firstname",
            "last_name": "customer lastname",
            "email": "update.customer@nomail.com",
            "phone": "1854788865",
            "country": 1,
            "state": 1,
            "city": 1,
            "zip_code": "380008",
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:customers-detail', args=(1,))
            response = self.client.put(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failed_update_customer_not_found(self):
        data = {
            "client": 1,
            "first_name": "customer firstname",
            "last_name": "customer lastname",
            "email": "update.customer@nomail.com",
            "phone": "1854788865",
            "country": 1,
            "state": 1,
            "city": 1,
            "zip_code": "380008",
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:customers-detail', args=(2,))
            response = self.client.put(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_customer(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:customers-detail', args=(1,))
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_customer_not_found(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('projects:customers-detail', args=(2,))
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
