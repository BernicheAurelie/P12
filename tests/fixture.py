from rest_framework.test import APITestCase
from users.models import User, User_role
from clients.models import Client
from contracts.models import Contract
from events.models import Event, Event_status


class TestSetUp(APITestCase):
    def setUp(self):
        self.user_role1 = User_role.objects.create(id=1, user_role="saler")
        self.user_role2 = User_role.objects.create(id=2, user_role="manager")
        self.user_role3 = User_role.objects.create(id=3, user_role="technician")

        role1 = User_role.objects.get(id=1)
        role2 = User_role.objects.get(id=2)
        role3 = User_role.objects.get(id=3)

        self.user1 = User.objects.create(
            first_name="test1",
            last_name="user1",
            username="test1",
            email="user1@test.com",
            role=role1,
            is_admin="True",
            password="test1234",
        )
        self.user1.set_password(self.user1.password)
        self.user1.save()

        self.user2 = User.objects.create(
            first_name="test2",
            last_name="user2",
            username="test2",
            email="user2@test.com",
            role=role2,
            is_admin="False",
            password="test1234",
        )
        self.user2.set_password(self.user2.password)
        self.user2.save()

        self.user3 = User.objects.create(
            first_name="test3",
            last_name="user3",
            username="test3",
            email="user3@test.com",
            role=role1,
            is_admin="False",
            password="test1234",
        )
        self.user3.set_password(self.user3.password)
        self.user3.save()

        self.manager_1 = User.objects.create(
            first_name="manager_1",
            last_name="manager_1",
            username="manager_1",
            email="manager_1@test.com",
            role=role2,
            is_admin="False",
            password="test1234",
        )
        self.manager_1.set_password(self.manager_1.password)
        self.manager_1.save()

        self.saler_1 = User.objects.create(
            first_name="saler_1",
            last_name="saler_1",
            username="saler_1",
            email="saler_1@test.com",
            role=role1,
            is_admin="False",
            password="test1234",
        )
        self.saler_1.set_password(self.saler_1.password)
        self.saler_1.save()

        self.technician_1 = User.objects.create(
            first_name="technician_1",
            last_name="technician_1",
            username="technician_1",
            email="technician_1@test.com",
            role=role3,
            is_admin="False",
            password="test1234",
        )
        self.technician_1.set_password(self.technician_1.password)
        self.technician_1.save()

        self.client_1 = Client.objects.create(
            first_name="client_1",
            last_name="client_1",
            email="client_1@test.com",
            phone="0123456789",
            company_name="company_1",
            sales_contact=self.saler_1,
        )
        self.client_2 = Client.objects.create(
            first_name="client_2",
            last_name="client_2",
            email="client_2@test.com",
            phone="0223456789",
            company_name="company_2",
            sales_contact=self.user1,
        )
        self.contract_1 = Contract.objects.create(
            client=self.client_1, saler_contact=self.saler_1, amount=250
        )
        self.contract_2 = Contract.objects.create(
            client=self.client_2, saler_contact=self.user1, amount=1000
        )
        self.event_status_1_upcoming = Event_status.objects.create(id=1, tag="upcoming")
        self.event_status_2_current = Event_status.objects.create(id=2, tag="current")
        self.event_status_3_finished = Event_status.objects.create(id=3, tag="finished")

        event_status_1_upcoming = Event_status.objects.get(id=1)
        event_status_2_current = Event_status.objects.get(id=2)
        event_status_3_finished = Event_status.objects.get(id=3)

        self.event_2 = Event.objects.create(
            client_id=self.client_2,
            support_contact=self.technician_1,
            contract=self.contract_2,
            attendees=15,
            event_status=event_status_1_upcoming,
            notes="ras",
        )
