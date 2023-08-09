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
class TestClient(TestSetUp):
    def test_CRUD_for_client_for_sales_contact(self):
        self.client.force_login(self.saler_1)
        response = self.client.get("/clients/")
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                "id": 4,
                "first_name": "client_1",
                "last_name": "client_1",
                "email": "client_1@test.com",
                "phone": "0123456789",
                "mobile": "",
                "company_name": "company_1",
                "date_created": response.json()[0]["date_created"],
                "date_updated": response.json()[0]["date_updated"],
                "existing": False,
                "sales_contact": self.saler_1.id,
            },
            {
                "id": 5,
                "first_name": "client_2",
                "last_name": "client_2",
                "email": "client_2@test.com",
                "phone": "0223456789",
                "mobile": "",
                "company_name": "company_2",
                "date_created": response.json()[1]["date_created"],
                "date_updated": response.json()[1]["date_updated"],
                "existing": False,
                "sales_contact": self.user1.id,
            },
        ]
        self.assertEqual(response.json(), expected)
        response1 = self.client.post(
            "/clients/",
            data={
                "first_name": "client12",
                "last_name": "client12",
                "email": "client12@test.com",
                "phone": "0923456789",
                "mobile": "",
                "company_name": "company12",
                "existing": False,
                "sales_contact": self.saler_1.id,
            },
        )
        self.assertEqual(response1.status_code, 201)
        response2 = self.client.get("/clients/")
        self.assertEqual(response2.json()[2]["first_name"], "client12")
        client12 = Client.objects.get(first_name="client12")
        self.client.put(
            "/clients/" + str(client12.id) + "/",
            data={
                "first_name": "client12_modified",
                "last_name": "client12",
                "email": "client12@test.com",
                "phone": "0923456789",
                "mobile": "",
                "company_name": "company12",
                "existing": False,
                "sales_contact": self.saler_1.id,
            },
        )
        response3 = self.client.get("/clients/")
        self.assertEqual(response3.json()[2]["first_name"], "client12_modified")
        response4 = self.client.delete("/clients/" + str(client12.id) + "/")
        response5 = self.client.get("/clients/" + str(client12.id) + "/")
        self.assertEqual(response5.data["detail"], "Not found.")
        response6 = self.client.post(
            "/clients/",
            data={
                "first_name": "new_client",
                "last_name": "new_client",
                "email": "new_client@test.com",
                "phone": "1023456789",
                "mobile": "",
                "company_name": "company12",
                "existing": False,
            },
        )
        self.assertEqual(response6.status_code, 201)
        new_client = Client.objects.get(first_name="new_client")
        response7 = self.client.get("/clients/" + str(new_client.id) + "/")
        self.assertEqual(response7.data["sales_contact"], self.saler_1.id)

    def test_post_client_forbidden_for_technician(self):
        self.client.force_login(self.technician_1)
        response5 = self.client.get("/clients/")
        self.assertEqual(response5.status_code, 200)
        response6 = self.client.patch(
            "/clients/" + str(self.client_2.id) + "/",
            data={"first_name": "updating_forbidden"},
        )
        self.assertEqual(response6.status_code, 403)
        self.assertEqual(
            response6.data["detail"],
            "You do not have permission to perform this action.",
        )
        response7 = self.client.delete("/clients/" + str(self.client_2.id) + "/")
        self.assertEqual(response7.status_code, 403)
        self.assertEqual(
            response7.data["detail"],
            "You do not have permission to perform this action.",
        )
        response = self.client.post(
            "/clients/",
            data={
                "first_name": "client12",
                "last_name": "client12",
                "email": "client12@test.com",
                "phone": "0923456789",
                "mobile": "",
                "company_name": "company12",
                "existing": False,
                "sales_contact": self.saler_1.id,
            },
        )
        print(response.data["detail"])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_CRUD_clients_for_manager(self):
        self.client.force_login(self.manager_1)
        response = self.client.get("/clients/")
        self.assertEqual(response.status_code, 200)
        response2 = self.client.post(
            "/clients/",
            data={
                "first_name": "new_client",
                "last_name": "new_client",
                "email": "new_client@test.com",
                "phone": "0323456789",
                "mobile": "",
                "company_name": "new_client_company",
                "existing": False,
                "sales_contact": self.saler_1.id,
            },
        )
        self.assertEqual(response2.status_code, 201)
        new_client = Client.objects.get(first_name="new_client")
        response3 = self.client.put(
            "/clients/" + str(new_client.id) + "/",
            data={
                "first_name": "new_client_modified",
                "last_name": "new_client",
                "email": "new_client@test.com",
                "phone": "0323456789",
                "mobile": "",
                "company_name": "company_2",
                "existing": False,
            },
        )
        self.assertEqual(response3.status_code, 200)
        response4 = self.client.get("/clients/" + str(new_client.id) + "/")
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(response4.json()["first_name"], "new_client_modified")
        self.assertEqual(response4.json()["sales_contact"], self.saler_1.id)
        response5 = self.client.delete("/clients/" + str(new_client.id) + "/")
        self.assertEqual(response5.status_code, 204)
        response6 = self.client.get("/clients/" + str(new_client.id) + "/")
        self.assertEqual(response6.status_code, 404)
        self.assertEqual(response6.data["detail"], "Not found.")

    def test_UD_forbidden_if_not_sales_contact(self):
        self.client.force_login(self.saler_1)
        response = self.client.put(
            "/clients/" + str(self.client_2.id) + "/",
            data={
                "first_name": "client_2_modified",
                "last_name": "client_2",
                "email": "client_2@test.com",
                "phone": "0223456789",
                "mobile": "",
                "company_name": "company_2",
                "existing": False,
                "sales_contact": self.user1.id,
            },
        )
        self.assertEqual(response.status_code, 403)
        response1 = self.client.delete("/clients/" + str(self.client_2.id) + "/")
        self.assertEqual(response1.status_code, 403)
        self.assertEqual(
            response1.data["detail"],
            "You do not have permission to perform this action.",
        )
        # self.client.force_login(self.technician_1)
        # response5 = self.client.get('/clients/')
        # self.assertEqual(response5.status_code, 200)
        # response6=self.client.patch('/clients/'+ str(self.client_2.id)+'/', data={'first_name': 'updating_forbidden'})
        # self.assertEqual(response6.status_code, 403)
        # self.assertEqual(response6.data['detail'], "You do not have permission to perform this action.")
        # response7=self.client.delete('/clients/'+ str(self.client_2.id)+'/')
        # self.assertEqual(response7.status_code, 403)
        # self.assertEqual(response7.data['detail'], "You do not have permission to perform this action.")
