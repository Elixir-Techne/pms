import io
from contextlib import contextmanager

from PIL import Image
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


class EmployeeTests(APITestCase):
    fixtures = ['user_auth.json', 'test_master.json', 'test_employees.json', 'test_employment.json']

    def test_create_employee_profile(self):
        user = '1'
        data = {
            "user": user,
            "first_name": "akash",
            "last_name": "patel",
            "gender": "male",
            "ssn": "ABCD1234",
            "birth_date": "2018-03-29",
            "address_1": "101,testing address1,test",
            "address_2": "202,testing address2,test",
            "country": "1",
            "state": "1",
            "city": "1",
            "zip_code": "380008",
            "phone": "9898222623",
            "status": "pending",
            "availability": "available"
        }

        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:profile-list')
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_employee_profile_failed(self):
        data = {
            "first_name": "akash",
            "last_name": "patel",
            "gender": "male",
            "ssn": "ABCD1234",
            "birth_date": "2018-03-29",
            "address_1": "101,testing address1,test",
            "address_2": "202,testing address2,test",
            "country": "1",
            "state": "1",
            "city": "1",
            "zip_code": "380008",
            "phone": "9898222623",
            "status": "pending",
            "availability": "available"
        }

        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:profile-list')
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_upload_employee_image(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:profile_image')
            photo_file = self.generate_photo_file()
            data = {
                'image': photo_file
            }
            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_employee_profile(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:profile-list')
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_employee(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:search_employee')
            response = self.client.post(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_failed_search(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:search_employee')
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_employee_profile(self):
        user = '2'
        data = {
            "user": user,
            "first_name": "akash",
            "last_name": "patel",
            "gender": "male",
            "ssn": "ABCD",
            "birth_date": "2018-03-29",
            "address_1": "101,testing address1,test",
            "address_2": "202,testing address2,test",
            "country": "1",
            "state": "1",
            "city": "1",
            "zip_code": "380008",
            "phone": "9898222623",
            "status": "pending",
            "availability": "available"
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:profile-detail', args=(7,))
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_failed_update_employee_profile(self):
        data = {
            "first_name": "akash",
            "last_name": "patel",
            "gender": "male",
            "ssn": "ABCD",
            "birth_date": "2018-03-29",
            "address_1": "101,testing address1,test",
            "address_2": "202,testing address2,test",
            "country": "1",
            "state": "1",
            "city": "1",
            "zip_code": "380008",
            "phone": "9898222623",
            "status": "pending",
            "availability": "available"
        }
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:profile-detail', args=(7,))
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_employee_profile(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:profile-detail', args=(7,))
            response = self.client.delete(url)
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_employee_full_profile(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:employee_details')
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_failed_get_employee_full_profile(self):
        with login(self.client, username='admin', password='akash@123'):
            url = reverse('employees:employee_details')
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_employment(self):
        employee = 6
        data = {
            "employee": employee,
            "company": "testpms",
            "location": "ahmedabad",
            "title": "test case",
            "start_date": "2018-03-28",
            "end_date": "2018-03-31",
            "department": "development",
            "compensation_type": "salaried",
            "employment_type": "full_time",
            "annual_salary": 100000,
            "job_duties": "handling developments",
            "flsa_classification": "abc",
            "manager": "abc",
            "direct_reports": "abc",
            "is_current": True,
            "notes": "test only"
        }

        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:employment_compensation-list')
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_failed_create_employment(self):
        data = {
            "company": "testpms",
            "location": "ahmedabad",
            "title": "test case",
            "start_date": "2018-03-28",
            "end_date": "2018-03-31",
            "department": "development",
            "compensation_type": "salaried",
            "employment_type": "full_time",
            "annual_salary": 100000,
            "job_duties": "handling developments",
            "flsa_classification": "abc",
            "manager": "abc",
            "direct_reports": "abc",
            "is_current": True,
            "notes": "test only"
        }

        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:employment_compensation-list')
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failed_get_employee_employment(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:employment_compensation-list')
            response = self.client.get(url)
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_employment(self):
        employee = 6
        data = {
            "employee": employee,
            "company": "testpms",
            "location": "ahmedabad",
            "title": "test case",
            "start_date": "2018-03-28",
            "end_date": "2018-03-31",
            "department": "development",
            "compensation_type": "salaried",
            "employment_type": "full_time",
            "annual_salary": 100000,
            "job_duties": "handling developments",
            "flsa_classification": "abc",
            "manager": "abc",
            "direct_reports": "abc",
            "is_current": True,
            "notes": "test only"
        }

        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:employment_compensation-detail', args=(2,))
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_failed_update_employment(self):
        data = {
            "company": "testpms",
            "location": "ahmedabad",
            "title": "test case",
            "start_date": "2018-03-28",
            "end_date": "2018-03-31",
            "department": "development",
            "compensation_type": "salaried",
            "employment_type": "full_time",
            "annual_salary": 100000,
            "job_duties": "handling developments",
            "flsa_classification": "abc",
            "manager": "abc",
            "direct_reports": "abc",
            "is_current": True,
            "notes": "test only"
        }

        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:employment_compensation-detail', args=(2,))
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_employee_employment(self):
        with login(self.client, username='test1', password='akash@123'):
            url = reverse('employees:employment_compensation-detail', args=(2,))
            response = self.client.delete(url)
            # print(response.__dict__)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
