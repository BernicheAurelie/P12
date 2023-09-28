import pytest
from tests.fixture import TestSetUp
from contracts.models import Contract


@pytest.mark.django_db
class TestContract(TestSetUp):
    def test_CRUD_contract_for_saler(self):
        self.client.force_login(self.saler_1)
        response = self.client.get("/contracts/")
        self.assertEqual(response.status_code, 200)
        response1 = self.client.get("/contracts/" + str(self.contract_1.id) + "/")
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.json()["saler_contact"], self.saler_1.id)
        response2 = self.client.put(
            "/contracts/" + str(self.contract_1.id) + "/",
            data={
                "client": self.client_1.id,
                "amount": 500,
            },
        )
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.data["result"]["amount"], "500")
        self.assertEqual(response2.data["message"], "Contract successfully updated")
        # get contract for others client but U and D forbidden
        response3 = self.client.get("/contracts/" + str(self.contract_2.id) + "/")
        self.assertEqual(response3.status_code, 200)
        response4 = self.client.put(
            "/contracts/" + str(self.contract_2.id) + "/",
            data={
                "client": self.client_2.id,
                "amount": 100,
            },
        )
        self.assertEqual(response4.status_code, 403)
        self.assertEqual(
            response4.data["detail"],
            "You do not have permission to perform this action.",
        )
        response5 = self.client.delete("/contracts/" + str(self.contract_2.id) + "/")
        self.assertEqual(response5.status_code, 403)
        self.assertEqual(
            response5.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_saler_can_post_new_contract_only_for_his_client(self):
        self.client.force_login(self.saler_1)
        response = self.client.post(
            "/contracts/",
            data={
                "client": self.client_1.id,
                "signed_status": "true",
                "amount": 100,
                "payment_due": "2023-10-04T13:39:47.825918Z",
            },
        )
        new_contract = Contract.objects.get(
            payment_due=response.data["result"]["payment_due"]
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Contract successfully created")
        self.assertEqual(new_contract.client.existing, True)
        response2 = self.client.post(
            "/contracts/",
            data={
                "client": self.client_2.id,
                "signed_status": "false",
                "amount": 100,
                "payment_due": "2025-01-01T13:39:47.825918Z",
            },
        )
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(
            response2.data["message"], "Forbidden, you're not in charge of this client."
        )
        empty_contract_list = Contract.objects.filter(
            payment_due="2025-01-01T13:39:47.825918Z"
        )
        self.assertEqual(empty_contract_list.count(), 0)

    def test_change_existing_status_for_client_when_contract_is_signed(self):
        self.client.force_login(self.saler_1)
        # with pytest.raises(KeyError, match=r".* signed status not given .*"):
        # with pytest.raises(KeyError) as excinfo:
        #     assert "signed status not given" in str(excinfo.value)
        response = self.client.post(
            "/contracts/",
            data={
                "client": self.client_1.id,
                "amount": 100,
                "payment_due": "2023-10-04T13:39:47.825918Z",
            },
        )
        new_contract = Contract.objects.get(
            payment_due=response.data["result"]["payment_due"]
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Contract successfully created")
        self.assertEqual(new_contract.client.existing, False)
        response2 = self.client.post(
            "/contracts/",
            data={
                "client": self.client_1.id,
                "signed_status": "false",
                "amount": 500,
                "payment_due": "2025-01-01T13:39:47.825918Z",
            },
        )
        self.assertEqual(response2.status_code, 200)
        second_contract = Contract.objects.get(
            payment_due=response2.data["result"]["payment_due"]
        )
        self.assertEqual(second_contract.client.existing, False)
        response3 = self.client.patch(
            "/contracts/" + str(second_contract.id) + "/",
            data={
                "client": self.client_1.id,
                "signed_status": "false",
                "amount": 200,
                # 'payment_due': "2025-01-01T13:39:47.825918Z"
            },
        )
        modified_contract = Contract.objects.get(
            payment_due="2025-01-01T13:39:47.825918Z"
        )
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.data["result"]["amount"], "200")
        self.assertEqual(response3.data["message"], "Contract successfully updated")
        self.assertEqual(modified_contract.client.existing, False)
        response4 = self.client.patch(
            "/contracts/" + str(second_contract.id) + "/",
            data={
                "client": self.client_1.id,
                "signed_status": "true",
                # "amount":500,
                # 'payment_due': "2025-01-01T13:39:47.825918Z"
            },
        )
        contract = Contract.objects.get(payment_due="2025-01-01T13:39:47.825918Z")
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(response4.data["message"], "Contract successfully updated")
        # self.assertEqual(second_contract.client.existing, True)
        self.assertEqual(contract.client.existing, True)
        response5 = self.client.patch(
            "/contracts/" + str(second_contract.id) + "/",
            data={
                "client": self.client_1.id,
                "signed_status": "false",
                # "amount":500,
                # 'payment_due': "2025-01-01T13:39:47.825918Z"
            },
        )
        patch_contract = Contract.objects.get(payment_due="2025-01-01T13:39:47.825918Z")
        self.assertEqual(response5.status_code, 200)
        self.assertEqual(response5.data["message"], "Contract successfully updated")
        # Existing status for client doesn't change
        self.assertEqual(patch_contract.client.existing, True)

    def test_CRUD_for_technician(self):
        self.client.force_login(self.technician_1)
        response = self.client.get("/contracts/")
        self.assertEqual(response.status_code, 200)
        res = self.client.post(
            "/contracts/",
            data={
                "client": self.client_1.id,
                "signed_status": "true",
                "amount": 100,
                "payment_due": "2024-01-01T13:39:47.825918Z",
                "saler_contact": self.saler_1.id,
            },
        )
        self.assertEqual(
            res.data["detail"], "You do not have permission to perform this action."
        )

    def test_CRUD_contract_for_admin(self):
        self.client.force_login(self.user1)
        response = self.client.get("/contracts/")
        self.assertEqual(response.status_code, 200)
        res = self.client.post(
            "/contracts/",
            data={
                "client": self.client_1.id,
                "signed_status": "true",
                "amount": 100,
                "payment_due": "2024-01-01T13:39:47.825918Z",
            },
        )
        self.assertEqual(
            res.data["message"],
            "saler_contact is required to create contract for managers or administrators",
        )
        response = self.client.post(
            "/contracts/",
            data={
                "client": self.client_1.id,
                "signed_status": "true",
                "amount": 100,
                "payment_due": "2024-01-01T13:39:47.825918Z",
                "saler_contact": self.saler_1.id,
            },
        )
        self.assertEqual(response.data["message"], "Contract successfully created")
        new_contract = Contract.objects.get(
            payment_due=response.data["result"]["payment_due"]
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_contract.client.existing, True)
        response2 = self.client.patch(
            "/contracts/" + str(new_contract.id) + "/",
            data={
                "client": self.client_1.id,
                "signed_status": "false",
                "amount": 600,
                "payment_due": "2024-01-01T13:39:47.825918Z",
            },
        )
        response3 = self.client.get("/contracts/" + str(new_contract.id) + "/")
        self.assertEqual(response3.json()["amount"], 600)
        self.assertEqual(new_contract.client.existing, True)
        response4 = self.client.patch(
            "/contracts/" + str(new_contract.id) + "/",
            data={
                "client": self.client_1.id,
                "amount": 1000,
                "payment_due": "2024-01-01T13:39:47.825918Z",
            },
        )
        response5 = self.client.get("/contracts/" + str(new_contract.id) + "/")
        self.assertEqual(response5.json()["amount"], 1000)
        self.assertEqual(new_contract.client.existing, True)
        response6 = self.client.delete("/contracts/" + str(new_contract.id) + "/")
        self.assertEqual(response6.status_code, 204)
        response7 = self.client.get("/contracts/" + str(new_contract.id) + "/")
        self.assertEqual(response7.data["detail"], "Not found.")

    def test_CRUD_contract_for_manager(self):
        self.client.force_login(self.manager_1)
        response = self.client.get("/contracts/")
        self.assertEqual(response.status_code, 200)
        res = self.client.post(
            "/contracts/",
            data={
                "client": self.client_1.id,
                "signed_status": "true",
                "amount": 100,
                "payment_due": "2024-01-01T13:39:47.825918Z",
            },
        )
        self.assertEqual(
            res.data["message"],
            "saler_contact is required to create contract for managers or administrators",
        )
        response = self.client.post(
            "/contracts/",
            data={
                "client": self.client_1.id,
                "signed_status": "true",
                "amount": 100,
                "payment_due": "2024-01-01T13:39:47.825918Z",
                "saler_contact": self.saler_1.id,
            },
        )
        self.assertEqual(response.data["message"], "Contract successfully created")
        new_contract = Contract.objects.get(
            payment_due=response.data["result"]["payment_due"]
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_contract.client.existing, True)
        response2 = self.client.patch(
            "/contracts/" + str(new_contract.id) + "/",
            data={
                "client": self.client_1.id,
                "signed_status": "true",
                "amount": 600,
                "payment_due": "2024-01-01T13:39:47.825918Z",
            },
        )
        response3 = self.client.get("/contracts/" + str(new_contract.id) + "/")
        self.assertEqual(response3.json()["amount"], 600)
        response4 = self.client.delete("/contracts/" + str(new_contract.id) + "/")
        self.assertEqual(response4.status_code, 204)
        response5 = self.client.get("/contracts/" + str(new_contract.id) + "/")
        self.assertEqual(response5.data["detail"], "Not found.")

    # def test_CRUD_contract_for_manager(self):
    #     self.client.force_login(self.manager_1)
    #     response=self.client.get('/contracts/')
    #     self.assertEqual(response.status_code, 200)
    #     response1 = self.client.post('/contracts/', data={
    #         "client":self.client_1.id,
    #         'signed_status': 'true',
    #         "amount":100,
    #         'payment_due': "2025-01-01T13:39:47.825918Z",
    #         "saler_contact": self.saler_1.id
    #     })
    #     self.assertEqual(response1.data["message"], "Contract successfully created")
    #     new_contract = Contract.objects.get(payment_due=response1.data['result']['payment_due'])
    #     self.assertEqual(response1.status_code, 200)
    #     self.assertEqual(new_contract.client.existing, True)
    #     response2 = self.client.patch('/contracts/'+ str(new_contract.id)+ '/', data={
    #         "client":self.client_1.id,
    #         'signed_status': 'true',
    #         "amount":600,
    #         'payment_due': "2030-01-01T13:39:47.825918Z"
    #     })
    #     response3 = self.client.get('/contracts/'+ str(new_contract.id)+ '/')
    #     self.assertEqual(response3.json()["amount"], 600)
    #     response4 = self.client.delete('/contracts/'+ str(new_contract.id)+ '/')
    #     self.assertEqual(response4.status_code, 204)
    #     response5 = self.client.get('/contracts/'+ str(new_contract.id)+ '/')
    #     self.assertEqual(response5.data["detail"], "Not found.")
