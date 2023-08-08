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
        expected = 'modified_name'
        # expected = {
        #         'first_name': 'modified_name', 'last_name': 'user', 'username': 'test', 'email': 'user@test.com', 
        #         'role': 1, 'is_admin': False, 'password': 'test1234'
        #     }
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(response4.json()['first_name'], expected)
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
        self.client.force_login(self.saler_1)
        response = self.client.get('/clients/')
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                'id': 10, 'first_name': 'client_1', 'last_name': 'client_1', 'email': 'client_1@test.com', 
                'phone': '0123456789', 'mobile': '', 'company_name': 'company_1', 
                'date_created': response.json()[0]["date_created"], 'date_updated': response.json()[0]["date_updated"], 
                'existing': False, 'sales_contact': self.saler_1.id
            }, {'id': 11, 'first_name': 'client_2', 'last_name': 'client_2', 'email': 'client_2@test.com', 
                'phone': '0223456789', 'mobile': '', 'company_name': 'company_2', 
                'date_created': response.json()[1]["date_created"], 'date_updated': response.json()[1]["date_updated"], 
                'existing': False, 'sales_contact': self.user1.id}
        ]
        self.assertEqual(response.json(), expected)
        self.client.post('/clients/', data=
            {
                'first_name': 'client12', 'last_name': 'client12', 'email': 'client12@test.com', 
                'phone': '0923456789', 'mobile': '', 'company_name': 'company12', 
                'existing': False, 'sales_contact': self.saler_1.id
            }
        )
        self.assertEqual(response.status_code, 200)
        response2 = self.client.get('/clients/')
        self.assertEqual(response2.json()[2]['first_name'], 'client12')
        client12 = Client.objects.get(first_name='client12')
        self.client.put('/clients/'+ str(client12.id)+'/', data={
            'first_name': 'client12_modified', 'last_name': 'client12', 'email': 'client12@test.com', 
                'phone': '0923456789', 'mobile': '', 'company_name': 'company12', 
                'existing': False, 'sales_contact': self.saler_1.id
        })
        response3 = self.client.get('/clients/')
        self.assertEqual(response3.json()[2]['first_name'], 'client12_modified')
        response4 = self.client.delete('/clients/'+ str(client12.id)+'/')
        response5 = self.client.get('/clients/'+ str(client12.id)+'/')
        self.assertEqual(response5.data['detail'], "Not found.")

    def test_CRUD_clients_for_manager(self):
        self.client.force_login(self.manager_1)
        response = self.client.get('/clients/')
        self.assertEqual(response.status_code, 200)
        response2 = self.client.post('/clients/', data=
            {
                'first_name': 'new_client', 'last_name': 'new_client', 'email': 'new_client@test.com', 
                'phone': '0323456789', 'mobile': '', 'company_name': 'new_client_company', 
                'existing': False, 'sales_contact': self.saler_1.id
            }
        )
        self.assertEqual(response2.status_code, 201)
        new_client = Client.objects.get(first_name='new_client')
        response3=self.client.put('/clients/'+ str(new_client.id)+'/', data=
                {
                    'first_name': 'new_client_modified', 'last_name': 'new_client', 'email': 'new_client@test.com', 
                    'phone': '0323456789', 'mobile': '', 'company_name': 'company_2', 
                    'existing': False, 'sales_contact': self.user1.id
                }
                                  )
        self.assertEqual(response3.status_code, 200)
        response4=self.client.get('/clients/'+ str(new_client.id)+'/')
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(response4.json()['first_name'], 'new_client_modified')
        response5=self.client.delete('/clients/'+ str(new_client.id)+'/')
        self.assertEqual(response5.status_code, 204)
        response6=self.client.get('/clients/'+ str(new_client.id)+'/')
        self.assertEqual(response6.status_code, 404)
        self.assertEqual(response6.data['detail'], "Not found.")

    def test_CRUD_forbidden(self):
        self.client.force_login(self.saler_1)
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
        response2 = self.client.put('/contracts/'+str(self.contract_1.id)+'/', data={
            "client":self.client_1.id,
            "amount":500,
        })
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.data['result']['amount'], '500')
        self.assertEqual(response2.data["message"], "Contract successfully updated")
        # get contract for others client but U and D forbidden
        response3 = self.client.get('/contracts/'+str(self.contract_2.id)+'/')
        self.assertEqual(response3.status_code, 200)
        response4 = self.client.put('/contracts/'+str(self.contract_2.id)+'/', data={
            "client":self.client_2.id,
            "amount":100,
        })
        self.assertEqual(response4.status_code, 403)
        self.assertEqual(response4.data['detail'], "You do not have permission to perform this action.")
        response5 = self.client.delete('/contracts/'+str(self.contract_2.id)+'/')
        self.assertEqual(response5.status_code, 403)
        self.assertEqual(response5.data['detail'], "You do not have permission to perform this action.")

    def test_saler_can_post_new_contract_only_for_his_client(self):
        self.client.force_login(self.saler_1)
        response = self.client.post('/contracts/', data={
            "client":self.client_1.id, 
            'signed_status': 'true',
            "amount":100,
            'payment_due': "2023-10-04T13:39:47.825918Z"
        })
        new_contract = Contract.objects.get(payment_due=response.data['result']['payment_due'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "Contract successfully created")
        self.assertEqual(new_contract.client.existing, True)
        # print("*********************** 2: self.client_1.existing *******************", self.client_1.existing)
        response2 = self.client.post('/contracts/', data={
            "client":self.client_2.id, 
            'signed_status': 'False',
            "amount":100,
            'payment_due': "2025-01-01T13:39:47.825918Z"
        })
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.data["message"], "Forbidden, you're not in charge of this client.")
        empty_contract_list = Contract.objects.filter(payment_due="2025-01-01T13:39:47.825918Z")
        self.assertEqual(empty_contract_list.count(), 0)

    def test_CRUD_contract_for_manager(self):
        self.client.force_login(self.manager_1)
        response=self.client.get('/contracts/')
        self.assertEqual(response.status_code, 200)
        response1 = self.client.post('/contracts/', data={
            "client":self.client_1.id, 
            'signed_status': 'true',
            "amount":100,
            'payment_due': "2025-01-01T13:39:47.825918Z",
            "saler_contact": self.saler_1.id
        })
        self.assertEqual(response1.data["message"], "Contract successfully created")
        new_contract = Contract.objects.get(payment_due=response1.data['result']['payment_due'])
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(new_contract.client.existing, True)
        response2 = self.client.patch('/contracts/'+ str(new_contract.id)+ '/', data={
            "client":self.client_1.id, 
            'signed_status': 'true',
            "amount":600,
            'payment_due': "2030-01-01T13:39:47.825918Z"
        })
        response3 = self.client.get('/contracts/'+ str(new_contract.id)+ '/')
        self.assertEqual(response3.json()["amount"], 600)
        response4 = self.client.delete('/contracts/'+ str(new_contract.id)+ '/')
        self.assertEqual(response4.status_code, 204)
        response5 = self.client.get('/contracts/'+ str(new_contract.id)+ '/')
        self.assertEqual(response5.data["detail"], "Not found.")

    def test_CRUD_contract_for_admin(self):
        self.client.force_login(self.user1)
        response=self.client.get('/contracts/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/contracts/', data={
            "client":self.client_1.id, 
            'signed_status': 'true',
            "amount":100,
            'payment_due': "2024-01-01T13:39:47.825918Z",
            "saler_contact": self.saler_1.id
        })
        self.assertEqual(response.data["message"], "Contract successfully created")
        new_contract = Contract.objects.get(payment_due=response.data['result']['payment_due'])
        print("************* new_contract.id, new_contract.saler_contact", new_contract.id, new_contract.saler_contact)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_contract.client.existing, True)
        response2 = self.client.patch('/contracts/'+ str(new_contract.id)+ '/', data={
            "client":self.client_1.id, 
            'signed_status': 'true',
            "amount":600,
            'payment_due': "2024-01-01T13:39:47.825918Z"
        })
        response3 = self.client.get('/contracts/'+ str(new_contract.id)+ '/')
        self.assertEqual(response3.json()["amount"], 600)
        response4 = self.client.delete('/contracts/'+ str(new_contract.id)+ '/')
        self.assertEqual(response4.status_code, 204)
        response5 = self.client.get('/contracts/'+ str(new_contract.id)+ '/')
        self.assertEqual(response5.data["detail"], "Not found.")

@pytest.mark.django_db
class TestEvent(TestSetUp):
    def test_get_event(self):
        self.client.force_login(self.saler_1)
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.manager_1)
        response2 = self.client.get('/events/')
        self.assertEqual(response2.status_code, 200)
        self.client.force_login(self.user1) # admin:
        response3 = self.client.get('/events/')
        self.assertEqual(response3.status_code, 200)
        self.client.force_login(self.technician_1)
        response4 = self.client.get('/events/')
        self.assertEqual(response4.status_code, 200)

    def test_get_an_event(self):
        self.client.force_login(self.saler_1)
        res = self.client.get('/events/')
        event_id = res.json()[0]['id']
        response = self.client.get('/events/'+str(event_id)+'/')
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.manager_1)
        response2 = self.client.get('/events/'+str(event_id)+'/')
        self.assertEqual(response2.status_code, 200)
        self.client.force_login(self.user1) # admin:
        response3 = self.client.get('/events/'+str(event_id)+'/')
        self.assertEqual(response3.status_code, 200)
        self.client.force_login(self.technician_1)
        response4 = self.client.get('/events/'+str(event_id)+'/')
        self.assertEqual(response4.status_code, 200)

    def test_create_event_for_contract_saler_contact_update_for_tech_support(self):
        self.client.force_login(self.saler_1)
        self.client.post('/contracts/', data={
            "client":self.client_1.id, 
            'signed_status': 'true',
            "amount":100,
            'payment_due': "2026-10-04T13:39:47.825918Z"
        })
        new_contract = Contract.objects.get(payment_due="2026-10-04T13:39:47.825918Z")
        response = self.client.post('/events/', data={
            "client_id":new_contract.client.id, "support_contact":self.technician_1.pk, 
            "contract":new_contract.id, "attendees":50,
            "event_status":1, 
            "event_date": "2024-01-01T12:00:47.825918Z", "notes":'anniversaire'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Event successfully created")
        new_event = Event.objects.get(event_date="2024-01-01T12:00:47.825918Z")
        response2 = self.client.patch('/events/'+ str(new_event.id) + '/', data={
            "client_id":new_contract.client.id, "support_contact":self.technician_1.pk, 
            "contract":new_contract.id, "attendees":25,
            "event_status":1, 
            "event_date": "2024-01-01T12:00:47.825918Z", "notes":'anniversaire'
        })
        self.assertEqual(response2.status_code, 403)
        self.assertEqual(response2.data['detail'], 'You do not have permission to perform this action.')
        self.client.force_login(self.technician_1)
        response3 = self.client.patch('/events/'+ str(new_event.id) + '/', data={
            "client_id":new_contract.client.id, "support_contact":self.technician_1.pk, 
            "contract":new_contract.id, "attendees":25,
            "event_status":1, 
            "event_date": "2024-01-01T12:00:47.825918Z", "notes":'anniversaire'
        })
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.data['result']['attendees'], '25')
        self.assertEqual(response3.data["message"], "Event successfully updated")
        # self.assertEqual(new_event.attendees, 25)
        response4 = self.client.delete('/events/'+ str(new_event.id) + '/')
        self.assertEqual(response4.status_code, 204)
        response5 = self.client.get('/events/'+ str(new_event.id) + '/')
        self.assertEqual(response5.status_code, 404)
        self.assertEqual(response5.data['detail'], 'Not found.')

    def test_CRUD_for_event_for_admin(self):
        self.client.force_login(self.user1) # admin
        self.client.post('/contracts/', data={
            "client":self.client_1.id, 
            'signed_status': 'true',
            "amount":100,
            'payment_due': "2026-10-04T13:39:47.825918Z",
            "saler_contact": self.saler_1.id
        })
        new_contract = Contract.objects.get(payment_due="2026-10-04T13:39:47.825918Z")
        response = self.client.post('/events/', data={
            "client_id":new_contract.client.id, "support_contact":self.technician_1.pk, 
            "contract":new_contract.id, "attendees":50,
            "event_status":1, 
            "event_date": "2024-01-01T12:00:47.825918Z", "notes":'anniversaire'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Event successfully created")
        new_event = Event.objects.get(event_date="2024-01-01T12:00:47.825918Z")
        response2 = self.client.patch('/events/'+ str(new_event.id) + '/', data={
            "client_id":new_contract.client.id, "support_contact":self.technician_1.pk, 
            "contract":new_contract.id, "attendees":25,
            "event_status":1, 
            "event_date": "2024-01-01T12:00:47.825918Z", "notes":'anniversaire'
        })
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.data['result']['attendees'], '25')
        self.assertEqual(response2.data["message"], "Event successfully updated")
        response3 = self.client.delete('/events/'+ str(new_event.id) + '/')
        self.assertEqual(response3.status_code, 204)
        response4 = self.client.get('/events/'+ str(new_event.id) + '/')
        self.assertEqual(response4.status_code, 404)
        self.assertEqual(response4.data['detail'], 'Not found.')

    def test_CRUD_for_event_for_manager(self):    
        self.client.force_login(self.manager_1) # manager
        self.client.post('/contracts/', data={
            "client":self.client_1.id, 
            'signed_status': 'true',
            "amount":100,
            'payment_due': "2026-10-04T13:39:47.825918Z",
            "saler_contact": self.saler_1.id
        })
        new_contract = Contract.objects.get(payment_due="2026-10-04T13:39:47.825918Z")
        response = self.client.post('/events/', data={
            "client_id":new_contract.client.id, "support_contact":self.technician_1.pk, 
            "contract":new_contract.id, "attendees":50,
            "event_status":1, 
            "event_date": "2024-01-01T12:00:47.825918Z", "notes":'anniversaire'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Event successfully created")
        new_event = Event.objects.get(event_date="2024-01-01T12:00:47.825918Z")
        response2 = self.client.patch('/events/'+ str(new_event.id) + '/', data={
            "client_id":new_contract.client.id, "support_contact":self.technician_1.pk, 
            "contract":new_contract.id, "attendees":25,
            "event_status":1, 
            "event_date": "2024-01-01T12:00:47.825918Z", "notes":'anniversaire'
        })
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.data['result']['attendees'], '25')
        self.assertEqual(response2.data["message"], "Event successfully updated")
        response3 = self.client.delete('/events/'+ str(new_event.id) + '/')
        self.assertEqual(response3.status_code, 204)
        response4 = self.client.get('/events/'+ str(new_event.id) + '/')
        self.assertEqual(response4.status_code, 404)
        self.assertEqual(response4.data['detail'], 'Not found.')
        