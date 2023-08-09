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
class TestEvent(TestSetUp):
    def test_get_event(self):
        self.client.force_login(self.saler_1)
        response = self.client.get("/events/")
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.manager_1)
        response2 = self.client.get("/events/")
        self.assertEqual(response2.status_code, 200)
        self.client.force_login(self.user1)  # admin:
        response3 = self.client.get("/events/")
        self.assertEqual(response3.status_code, 200)
        self.client.force_login(self.technician_1)
        response4 = self.client.get("/events/")
        self.assertEqual(response4.status_code, 200)

    def test_get_an_event(self):
        self.client.force_login(self.saler_1)
        res = self.client.get("/events/")
        event_id = res.json()[0]["id"]
        response = self.client.get("/events/" + str(event_id) + "/")
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.manager_1)
        response2 = self.client.get("/events/" + str(event_id) + "/")
        self.assertEqual(response2.status_code, 200)
        self.client.force_login(self.user1)  # admin:
        response3 = self.client.get("/events/" + str(event_id) + "/")
        self.assertEqual(response3.status_code, 200)
        self.client.force_login(self.technician_1)
        response4 = self.client.get("/events/" + str(event_id) + "/")
        self.assertEqual(response4.status_code, 200)

    def test_create_event_for_contract_saler_contact_update_for_tech_support(self):
        self.client.force_login(self.saler_1)
        self.client.post(
            "/contracts/",
            data={
                "client": self.client_1.id,
                "signed_status": "true",
                "amount": 100,
                "payment_due": "2026-10-04T13:39:47.825918Z",
            },
        )
        new_contract = Contract.objects.get(payment_due="2026-10-04T13:39:47.825918Z")
        response = self.client.post(
            "/events/",
            data={
                "client_id": new_contract.client.id,
                "support_contact": self.technician_1.pk,
                "contract": new_contract.id,
                "attendees": 50,
                "event_status": 1,
                "event_date": "2024-01-01T12:00:47.825918Z",
                "notes": "anniversaire",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Event successfully created")
        new_event = Event.objects.get(event_date="2024-01-01T12:00:47.825918Z")
        response2 = self.client.patch(
            "/events/" + str(new_event.id) + "/",
            data={
                "client_id": new_contract.client.id,
                "support_contact": self.technician_1.pk,
                "contract": new_contract.id,
                "attendees": 25,
                "event_status": 1,
                "event_date": "2024-01-01T12:00:47.825918Z",
                "notes": "anniversaire",
            },
        )
        self.assertEqual(response2.status_code, 403)
        self.assertEqual(
            response2.data["detail"],
            "You do not have permission to perform this action.",
        )
        self.client.force_login(self.technician_1)
        response3 = self.client.patch(
            "/events/" + str(new_event.id) + "/",
            data={
                "client_id": new_contract.client.id,
                "support_contact": self.technician_1.pk,
                "contract": new_contract.id,
                "attendees": 25,
                "event_status": 1,
                "event_date": "2024-01-01T12:00:47.825918Z",
                "notes": "anniversaire",
            },
        )
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.data["result"]["attendees"], "25")
        self.assertEqual(response3.data["message"], "Event successfully updated")
        # self.assertEqual(new_event.attendees, 25)
        response4 = self.client.delete("/events/" + str(new_event.id) + "/")
        self.assertEqual(response4.status_code, 204)
        response5 = self.client.get("/events/" + str(new_event.id) + "/")
        self.assertEqual(response5.status_code, 404)
        self.assertEqual(response5.data["detail"], "Not found.")

    def test_create_event_forbidden_if_not_contract_saler_contact(self):
        self.client.force_login(self.saler_1)
        self.client.post(
            "/contracts/",
            data={
                "client": self.client_1.id,
                "signed_status": "true",
                "amount": 201,
                "payment_due": "2024-02-12T13:39:47.825918Z",
            },
        )
        new_contract = Contract.objects.get(payment_due="2024-02-12T13:39:47.825918Z")
        print("new_contract.saler_contact", new_contract.saler_contact)
        self.client.force_login(self.user3)  # other saler non admin
        res = self.client.post(
            "/events/",
            data={
                "client_id": new_contract.client.id,
                "support_contact": self.technician_1.pk,
                "contract": new_contract.id,
                "attendees": 50,
                "event_status": 1,
                "event_date": "2024-01-01T12:00:47.825918Z",
                "notes": "anniversaire",
            },
        )
        print(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(
            res.data["detail"], "You do not have permission to perform this action."
        )

    def test_CRUD_for_event_for_admin(self):
        self.client.force_login(self.user1)  # admin
        self.client.post(
            "/contracts/",
            data={
                "client": self.client_1.id,
                "signed_status": "true",
                "amount": 100,
                "payment_due": "2026-10-04T13:39:47.825918Z",
                "saler_contact": self.saler_1.id,
            },
        )
        new_contract = Contract.objects.get(payment_due="2026-10-04T13:39:47.825918Z")
        response = self.client.post(
            "/events/",
            data={
                "client_id": new_contract.client.id,
                "support_contact": self.technician_1.pk,
                "contract": new_contract.id,
                "attendees": 50,
                "event_status": 1,
                "event_date": "2024-01-01T12:00:47.825918Z",
                "notes": "anniversaire",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Event successfully created")
        new_event = Event.objects.get(event_date="2024-01-01T12:00:47.825918Z")
        response2 = self.client.patch(
            "/events/" + str(new_event.id) + "/",
            data={
                "client_id": new_contract.client.id,
                "support_contact": self.technician_1.pk,
                "contract": new_contract.id,
                "attendees": 25,
                "event_status": 1,
                "event_date": "2024-01-01T12:00:47.825918Z",
                "notes": "anniversaire",
            },
        )
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.data["result"]["attendees"], "25")
        self.assertEqual(response2.data["message"], "Event successfully updated")
        response3 = self.client.delete("/events/" + str(new_event.id) + "/")
        self.assertEqual(response3.status_code, 204)
        response4 = self.client.get("/events/" + str(new_event.id) + "/")
        self.assertEqual(response4.status_code, 404)
        self.assertEqual(response4.data["detail"], "Not found.")

    def test_CRUD_for_event_for_manager(self):
        self.client.force_login(self.manager_1)  # manager
        self.client.post(
            "/contracts/",
            data={
                "client": self.client_1.id,
                "signed_status": "true",
                "amount": 100,
                "payment_due": "2026-10-04T13:39:47.825918Z",
                "saler_contact": self.saler_1.id,
            },
        )
        new_contract = Contract.objects.get(payment_due="2026-10-04T13:39:47.825918Z")
        response = self.client.post(
            "/events/",
            data={
                "client_id": new_contract.client.id,
                "support_contact": self.technician_1.pk,
                "contract": new_contract.id,
                "attendees": 50,
                "event_status": 1,
                "event_date": "2024-01-01T12:00:47.825918Z",
                "notes": "anniversaire",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Event successfully created")
        new_event = Event.objects.get(event_date="2024-01-01T12:00:47.825918Z")
        response2 = self.client.patch(
            "/events/" + str(new_event.id) + "/",
            data={
                "client_id": new_contract.client.id,
                "support_contact": self.technician_1.pk,
                "contract": new_contract.id,
                "attendees": 25,
                "event_status": 1,
                "event_date": "2024-01-01T12:00:47.825918Z",
                "notes": "anniversaire",
            },
        )
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.data["result"]["attendees"], "25")
        self.assertEqual(response2.data["message"], "Event successfully updated")
        response3 = self.client.delete("/events/" + str(new_event.id) + "/")
        self.assertEqual(response3.status_code, 204)
        response4 = self.client.get("/events/" + str(new_event.id) + "/")
        self.assertEqual(response4.status_code, 404)
        self.assertEqual(response4.data["detail"], "Not found.")
