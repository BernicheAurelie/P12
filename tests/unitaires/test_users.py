import pytest
from tests.fixture import TestSetUp
from users.models import User


@pytest.mark.django_db
class TestUsers(TestSetUp):
    def test_CRUD_users_for_admin_user(self):
        # login admin saler
        self.client.force_login(self.user1)
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)
        nbr_users = len(response.json())
        response1 = self.client.post(
            "/users/",
            data={
                "first_name": "test",
                "last_name": "user",
                "username": "test",
                "email": "user@test.com",
                "role": 1,
                "is_admin": "False",
                "password": "test1234",
            },
        )
        self.assertEqual(response1.status_code, 201)
        response2 = self.client.get("/users/")
        self.assertEqual(len(response2.json()), nbr_users+1)
        self.assertEqual(response2.status_code, 200)
        user = User.objects.get(username="test")
        url=("/users/" + str(user.id) + "/")
        res = self.client.put(
            f"{url}",
            data={
                "first_name": "test",
                "last_name": "user",
                "username": "modified_username",
                "email": "user@test.com",
                "role": 1,
                "is_admin": "False",
                "password":str(user.password),
            },
        )
        response3 = self.client.patch(
            f"{url}",
            data={
                "first_name": "modified_first_name",
            },
        )
        self.assertEqual(response3.status_code, 200)
        response4 = self.client.get(f"{url}")
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(response4.json()["first_name"], "modified_first_name")
        self.assertEqual(response4.json()["username"], "modified_username")
        response5 = self.client.delete(f"{url}")
        self.assertEqual(response5.status_code, 204)
        response6 = self.client.get(f"{url}")
        self.assertEqual(response6.data["detail"], "Not found.")

    def test_CRUD_users_for_manager(self):
        self.client.force_login(self.manager_1)
        response1 = self.client.get("/users/")
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.post(
            "/users/",
            data={
                "first_name": "test",
                "last_name": "user",
                "username": "test",
                "email": "test@test.com",
                "role": 1,
                "is_admin": "False",
                "password": "test1234",
            },
        )
        self.assertEqual(response2.status_code, 201)
        user = User.objects.get(first_name="test")
        response3 = self.client.put(
            "/users/" + str(user.id) + "/",
            data={
                "first_name": "test",
                "last_name": "user",
                "username": "modified_username",
                "email": "test@test.com",
                "role": 1,
                "is_admin": "False",
                "password": "test1234",
            },
        )
        self.assertEqual(response3.status_code, 200)
        response4 = self.client.get("/users/" + str(user.id) + "/")
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(response4.json()["username"], "modified_username")
        response5 = self.client.patch(
            "/users/" + str(user.id) + "/",
            data={
                "first_name": "test",
                "last_name": "user",
                "username": "username",
                "email": "test@test.com",
                "role": 1,
                "is_admin": "False",
            },
        )
        self.assertEqual(response5.status_code, 200)
        response6 = self.client.get("/users/" + str(user.id) + "/")
        self.assertEqual(response6.status_code, 200)
        self.assertEqual(response6.json()["username"], "username")

    def test_CRUD_users_forbidden_except_for_himself(self):
        # get and modify your profile but not delete it
        self.client.force_login(self.saler_1)
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 403)
        response2 = self.client.get("/users/" + str(self.saler_1.id) + "/")
        self.assertEqual(response2.status_code, 200)
        response3 = self.client.patch(
            "/users/" + str(self.saler_1.id) + "/",
            data={
                "first_name": "THE saler!",
            },
        )
        self.assertEqual(response3.status_code, 200)
        response4 = self.client.get("/users/" + str(self.saler_1.id) + "/")
        self.assertEqual(response4.json()["first_name"], "THE saler!")
        response5 = self.client.delete("/users/" + str(self.saler_1.id) + "/")
        self.assertEqual(
            response5.data["detail"],
            "You do not have permission to perform this action.",
        )
        self.assertEqual(response5.status_code, 403)
        self.client.force_login(self.technician_1)
        response6 = self.client.get("/users/")
        self.assertEqual(response6.status_code, 403)
