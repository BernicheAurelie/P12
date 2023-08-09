import pytest
from django.shortcuts import get_object_or_404
from rest_framework.test import APITestCase
from tests.fixture import TestSetUp
import tests.mocks as mock
from users.models import User
from clients.models import Client
from contracts.models import Contract
from events.models import Event

@pytest.mark.django_db
class TestUsers(TestSetUp):
    
    def test_CRUD_users_for_admin_user(self):
        # login admin saler
        self.client.force_login(self.user1)
        response1 = self.client.get('/users/')
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.post('/users/', data=
            {
                "first_name": "test",
                "last_name": "user",
                "username": "test",
                "email": "user@test.com",
                "role": 1,
                "is_admin" : "False",
                "password": "test1234"
            }
        )
        self.assertEqual(response2.status_code, 201)
        user = User.objects.get(first_name="test")
        response3 = self.client.put('/users/'+str(user.id)+'/', data=
            {
                "first_name": "modified_name",
                "last_name": "user",
                "username": "test",
                "email": "user@test.com",
                "role": 1,
                "is_admin" : "False",
                "password": "test1234"
            }
        )
        self.assertEqual(response3.status_code, 200)
        response4 = self.client.get('/users/'+str(user.id)+'/')
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(response4.json()['first_name'], "modified_name")
        response5 = self.client.delete('/users/'+str(user.id)+'/')
        self.assertEqual(response5.status_code, 204)
        response6 = self.client.get('/users/'+str(user.id)+'/')
        self.assertEqual(response6.data['detail'], "Not found.")

    def test_CRUD_users_for_manager(self):
        self.client.force_login(self.manager_1)
        response1 = self.client.get('/users/')
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.post('/users/', data=
            {
                "first_name": "test",
                "last_name": "user",
                "username": "test",
                "email": "test@test.com",
                "role": 1,
                "is_admin" : "False",
                "password": "test1234"
            }
        )
        
        self.assertEqual(response2.status_code, 201)
        user = User.objects.get(first_name="test")
        response3 = self.client.put('/users/'+str(user.id)+'/', data=
            {
                "first_name": "test",
                "last_name": "user",
                "username": "modified_username",
                "email": "test@test.com",
                "role": 1,
                "is_admin" : "False",
                "password": "test1234"
            }
        )
        self.assertEqual(response3.status_code, 200)
        response4 = self.client.get('/users/'+str(user.id)+'/')
        expected = {
                "first_name": "test",
                "last_name": "user",
                "username": "modified_username",
                "email": "test@test.com",
                "role": 1,
                "is_admin" : False,
                "password": "test1234"
            }
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(response4.json(), expected)
        response5 = self.client.patch('/users/'+str(user.id)+'/', data=
            {
                "first_name": "test",
                "last_name": "user",
                "username": "username",
                "email": "test@test.com",
                "role": 1,
                "is_admin" : "False",
            }
        )
        self.assertEqual(response5.status_code, 200)
        response6 = self.client.get('/users/'+str(user.id)+'/')
        expected_password = {
                "first_name": "test",
                "last_name": "user",
                "username": "username",
                "email": "test@test.com",
                "role": 1,
                "is_admin" : False,
                "password": "test1234"
            }
        self.assertEqual(response6.status_code, 200)
        self.assertEqual(response6.json(), expected_password)


    def test_CRUD_users_forbidden_except_for_himself(self):
        # get and modify your profile but not delete it
        self.client.force_login(self.saler_1)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 403)
        response2 = self.client.get('/users/'+ str(self.saler_1.id) + '/')
        self.assertEqual(response2.status_code, 200)
        response3 = self.client.put('/users/'+ str(self.saler_1.id) + '/', data={
                "first_name":"THE saler!",
                "last_name": "saler_1",
                "username": "saler_1",
                "email": "saler_1@test.com",
                "role": 1,
                "is_admin" : "False",
                "password": "test1234"
            }
        )
        self.assertEqual(response3.status_code, 200)
        response4 = self.client.get('/users/'+ str(self.saler_1.id) + '/')
        expected = {
            'first_name': 'THE saler!', 'last_name': 'saler_1', 
            'username': 'saler_1', 'password': 'test1234', 
            'email': 'saler_1@test.com', 'role': 1, 'is_admin': False
            }
        self.assertEqual(response4.json(), expected)
        response5 = self.client.delete('/users/'+ str(self.saler_1.id) + '/')
        self.assertEqual(response5.data['detail'], "You do not have permission to perform this action.")
        self.assertEqual(response5.status_code, 403)
        self.client.force_login(self.technician_1)
        response6 = self.client.get('/users/')
        self.assertEqual(response6.status_code, 403)
