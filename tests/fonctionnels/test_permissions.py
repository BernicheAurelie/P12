import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from tests.fonctionnels.test_setup import TestSetUp


class TestPermissions(TestSetUp):
    
    def test_salers_cannot_read_users(self):
        self.browser.get("http://127.0.0.1:8000/authentification/login/")
        form_username = self.browser.find_element_by_id("id_username")
        form_username.send_keys("fred")
        form_password = self.browser.find_element_by_id("id_password")
        form_password.send_keys("fred1234")
        login = self.browser.find_element_by_id("submit-id-submit")
        login.click()
        self.browser.get("http://127.0.0.1:8000/users/")
        permission_denied = self.browser.find_elements_by_css_selector('span.str')[1]
        self.assertEqual(permission_denied.text, '"You do not have permission to perform this action."')

    def test_technicians_cannot_read_users(self):
        self.browser.get("http://127.0.0.1:8000/authentification/login/")
        form_username = self.browser.find_element_by_id("id_username")
        form_username.send_keys("lila")
        form_password = self.browser.find_element_by_id("id_password")
        form_password.send_keys("lila1234")
        login = self.browser.find_element_by_id("submit-id-submit")
        login.click()
        self.browser.get("http://127.0.0.1:8000/users/")
        permission_denied = self.browser.find_elements_by_css_selector('span.str')[1]
        self.assertEqual(permission_denied.text, '"You do not have permission to perform this action."')
