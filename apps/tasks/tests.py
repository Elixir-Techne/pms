from contextlib import contextmanager

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


@contextmanager
def login(client, username='test1', password='test1@password'):
    url = reverse('rest_login')
    response = client.post(url, {'username': username, 'password': password}, format='json')
    token = response.data['token']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    yield
    client.credentials()


class TaskCategoryTests(APITestCase):
    fixtures = ['user_auth.json', 'test_master.json', 'test_employees.json', 'test_employment.json',
                'test_clients.json', 'test_manager.json', 'test_project.json', 'test_task.json']

    def test_create_task(self):
        data = {
            "name": "DI Task 1",
            "description": "This is task test case."
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('tasks:category-list')
            response = self.client.post(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tasks(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('tasks:category-list')
            response = self.client.get(url)
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_tasks(self):
        data = {
            "name": "DI Task 2",
            "description": "task test"
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('tasks:category-detail', args=(1,))
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_failed_update_tasks(self):
        data = {
            "name": "DI Task 2",
            "description": "task test"
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('tasks:category-detail', args=(2,))
            response = self.client.put(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('tasks:category-detail', args=(1,))
            response = self.client.delete(url)
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TaskTests(APITestCase):
    fixtures = ['user_auth.json', 'test_master.json', 'test_employees.json', 'test_employment.json',
                'test_clients.json', 'test_manager.json', 'test_project.json', 'test_task.json']

    def test_create_task(self):
        data = {
            "project": 1,
            "title": "pms task 1",
            "category": 1,
            "description": "task 1 description",
            "creator": 6,
            "assign": 7,
            "start_date": "2018-03-03",
            "end_date": "2019-03-03",
            "effort": 1.00
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('tasks:tasks-list')
            response = self.client.post(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_failed_create_task(self):
        data = {
            "project": 1,
            "title": "pms task 1",
            "category": 1,
            "description": "task 1 description",
            "creator": 1,
            "assign": 1,
            "start_date": "2018-03-03",
            "end_date": "2019-03-03",
            "effort": 1.00
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('tasks:tasks-list')
            response = self.client.post(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_tasks(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('tasks:tasks-list')
            response = self.client.get(url)
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task(self):
        data = {
            "project": 1,
            "title": "pms task 1",
            "category": 1,
            "description": "task 1 description",
            "creator": 6,
            "assign": 7,
            "start_date": "2018-03-03",
            "end_date": "2019-03-03",
            "effort": 1.00
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('tasks:tasks-detail', args=(1,))
            response = self.client.put(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_failed_update_task(self):
        data = {
            "project": 1,
            "title": "pms task 1",
            "category": 1,
            "description": "task 1 description",
            "creator": 1,
            "assign": 1,
            "start_date": "2018-03-03",
            "end_date": "2019-03-03",
            "effort": 1.00
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('tasks:tasks-detail', args=(1,))
            response = self.client.put(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failed_update_task_not_found(self):
        data = {
            "project": 1,
            "title": "pms task 1",
            "category": 1,
            "description": "task 1 description",
            "creator": 1,
            "assign": 1,
            "start_date": "2018-03-03",
            "end_date": "2019-03-03",
            "effort": 1.00
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('tasks:tasks-detail', args=(2,))
            response = self.client.put(url, data, format='json')
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('tasks:tasks-detail', args=(1,))
            response = self.client.delete(url)
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
