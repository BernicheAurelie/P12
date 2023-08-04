import pytest
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
        response3 = self.client.put('/users/7/', data=
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
        response4 = self.client.get('/users/7/')
        expected = {
                'first_name': 'modified_name', 'last_name': 'user', 'username': 'test', 'email': 'user@test.com', 
                'role': 1, 'is_admin': False, 'password': 'test1234'
            }
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(response4.json(), expected)
        response5 = self.client.delete('/users/7/')
        self.assertEqual(response5.status_code, 204)
        response6 = self.client.get('/users/7/')
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
        response3 = self.client.put('/users/14/', data=
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
        response4 = self.client.get('/users/14/')
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

@pytest.mark.django_db
class TestClient(TestSetUp):

    def test_CRUD_for_client_for_sales_contact(self):
        self.client.force_login(self.saler_1) # id 1?
        response = self.client.get('/clients/')
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                'id': 7, 'first_name': 'client_1', 'last_name': 'client_1', 'email': 'client_1@test.com', 
                'phone': '0123456789', 'mobile': '', 'company_name': 'company_1', 
                'date_created': response.json()[0]["date_created"], 'date_updated': response.json()[0]["date_updated"], 
                'existing': False, 'sales_contact': self.saler_1.id
            }, {'id': 8, 'first_name': 'client_2', 'last_name': 'client_2', 'email': 'client_2@test.com', 
                'phone': '0223456789', 'mobile': '', 'company_name': 'company_2', 
                'date_created': response.json()[1]["date_created"], 'date_updated': response.json()[1]["date_updated"], 
                'existing': False, 'sales_contact': self.user1.id}
        ]
        self.assertEqual(response.json(), expected)
        self.client.post('/clients/', data=
            {
                'first_name': 'client_9', 'last_name': 'client_9', 'email': 'client_9@test.com', 
                'phone': '0923456789', 'mobile': '', 'company_name': 'company_9', 
                'existing': False, 'sales_contact': self.saler_1.id
            }
        )
        self.assertEqual(response.status_code, 200)
        response2 = self.client.get('/clients/')
        self.assertEqual(response2.json()[2]['first_name'], 'client_9')
        client_9 = Client.objects.get(first_name='client_9')
        self.client.put('/clients/'+ str(client_9.id)+'/', data={
            'first_name': 'client_9_modified', 'last_name': 'client_9', 'email': 'client_9@test.com', 
                'phone': '0923456789', 'mobile': '', 'company_name': 'company_9', 
                'existing': False, 'sales_contact': self.saler_1.id
        })
        response3 = self.client.get('/clients/')
        self.assertEqual(response3.json()[2]['first_name'], 'client_9_modified')
        response4 = self.client.delete('/clients/'+ str(client_9.id)+'/')
        response5 = self.client.get('/clients/'+ str(client_9.id)+'/')
        self.assertEqual(response5.data['detail'], "Not found.")

    def test_CRUD_forbidden(self):
        self.client.force_login(self.saler_1)
        # client_2_user1_for_saler = Client.objects.get(first_name='client_2')
        response=self.client.put('/clients/'+ str(self.client_2.id)+'/', data=
                {
                    'first_name': 'client_2_modified', 'last_name': 'client_2', 'email': 'client_2@test.com', 
                    'phone': '0223456789', 'mobile': '', 'company_name': 'company_2', 
                    'existing': False, 'sales_contact': self.user1.id
                }
        )
        self.assertEqual(response.status_code, 403)
        response1=self.client.delete('/clients/'+ str(self.client_2.id)+'/')
        self.assertEqual(response1.status_code, 403)
        self.assertEqual(response1.data['detail'], "You do not have permission to perform this action.")
        self.client.force_login(self.manager_1)
        response2 = self.client.get('/clients/')
        self.assertEqual(response2.status_code, 200)
        response3=self.client.patch('/clients/'+ str(self.client_2.id)+'/', data={'first_name': 'updating_forbidden'})
        self.assertEqual(response3.status_code, 403)
        self.assertEqual(response3.data['detail'], "You do not have permission to perform this action.")
        response4=self.client.delete('/clients/'+ str(self.client_2.id)+'/')
        self.assertEqual(response4.status_code, 403)
        self.assertEqual(response4.data['detail'], "You do not have permission to perform this action.")
        self.client.force_login(self.technician_1)
        response5 = self.client.get('/clients/')
        self.assertEqual(response5.status_code, 200)
        response6=self.client.patch('/clients/'+ str(self.client_2.id)+'/', data={'first_name': 'updating_forbidden'})
        self.assertEqual(response6.status_code, 403)
        self.assertEqual(response6.data['detail'], "You do not have permission to perform this action.")
        response7=self.client.delete('/clients/'+ str(self.client_2.id)+'/')
        self.assertEqual(response7.status_code, 403)
        self.assertEqual(response7.data['detail'], "You do not have permission to perform this action.")

@pytest.mark.django_db
class TestContract(TestSetUp):

    def test_CRUD_contract_for_saler(self):
        self.client.force_login(self.saler_1)
        response = self.client.get('/contracts/')
        self.assertEqual(response.status_code, 200)
        response1 = self.client.get('/contracts/'+str(self.contract_1.id)+'/')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.json()['saler_contact'], self.saler_1.id)
        date_created = TestSetUp.created(self,response)
        date_updated =TestSetUp.updated(self, response)
        response2 = self.client.patch('/contracts/'+str(self.contract_1.id)+'/', data={
            "client":self.client_1.id, 
            'date_created': f"{date_created}",
            'date_updated':f"{date_updated}",
            'signed_status': 'False',
            "saler_contact":self.saler_1.id,
            "amount":"500",
            'payment_due': response1.json()['payment_due']
        })
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.json()['amount'], 500.0)
        # get contract for associated client 
        response3 = self.client.get('/contracts/'+str(self.contract_2.id)+'/')
        self.assertEqual(response3.status_code, 200)
        response4 = self.client.get('/contracts/'+str(self.contract_3.id)+'/')
        self.assertEqual(response4.status_code, 200)
        response5 = self.client.delete('/contracts/'+str(self.contract_3.id)+'/')
        self.assertEqual(response5.status_code, 403)
        self.assertEqual(response5.data['detail'], "You do not have permission to perform this action.")

    def test_CRUD_contract_forbidden(self):
        self.client.force_login(self.manager_1)
        response=self.client.get('/contracts/')
        self.assertEqual(response.status_code, 200)

# @pytest.mark.django_db
# class TestEvent(TestSetUp):
#     def test_get_event(self):
#         self.client.force_login(self.technician_1)
#         response = self.client.get('/events/')
#         self.assertEqual(response.status_code, 200)
