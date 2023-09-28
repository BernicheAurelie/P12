import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from tests.fonctionnels.test_setup import TestSetUp


class TestAuthentification(TestSetUp):
    def test_open_chrome_window(self):
        time.sleep(10)
        self.browser.get("http://127.0.0.1:8000/authentification/login/")
        title = self.browser.find_element_by_tag_name('h3')
        assert "Django REST framework" in title.text


    def test_authentification_and_redirection_to_clients(self):
        self.browser.get("http://127.0.0.1:8000/authentification/login/")
        form_username = self.browser.find_element_by_id("id_username")
        form_username.send_keys("fred")
        form_password = self.browser.find_element_by_id("id_password")
        form_password.send_keys("fred1234")
        form_password.send_keys(Keys.RETURN)
        self.assertEqual(self.browser.find_element_by_class_name("dropdown-toggle").text, "fred")
        self.assertEqual(self.browser.find_element_by_tag_name('h1').text, "Client List")
        self.assertEqual(self.browser.current_url, "http://127.0.0.1:8000/clients/")

    def test_wrong_username_to_authentication(self):
        self.browser.get("http://127.0.0.1:8000/authentification/login/")
        form_username = self.browser.find_element_by_id("id_username")
        form_username.send_keys("wrong_username")
        form_password = self.browser.find_element_by_id("id_password")
        form_password.send_keys("fred1234")
        form_password.send_keys(Keys.RETURN)
        error_message = self.browser.find_element_by_class_name("text-error")
        self.assertEqual(error_message.text, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
        self.assertEqual(self.browser.current_url, "http://127.0.0.1:8000/authentification/login/")

    def test_wrong_password_to_authentication(self):
        self.browser.get("http://127.0.0.1:8000/authentification/login/")
        form_username = self.browser.find_element_by_id("id_username")
        form_username.send_keys("fred")
        form_password = self.browser.find_element_by_id("id_password")
        form_password.send_keys("blabla")
        form_password.send_keys(Keys.RETURN)
        error_message = self.browser.find_element_by_class_name("text-error")
        self.assertEqual(error_message.text, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
        self.assertEqual(self.browser.current_url, "http://127.0.0.1:8000/authentification/login/")

    
    def test_admin_authentification(self):
        self.browser.get("http://127.0.0.1:8000/admin/login/")
        form_username = self.browser.find_element_by_id("id_username")
        form_username.send_keys("aurel")
        form_password = self.browser.find_element_by_id("id_password")
        form_password.send_keys("a20081113b")
        login_button = self.browser.find_element(By.XPATH, "//input[@type='submit']")
        login_button.click()
        self.assertEqual(self.browser.current_url, "http://127.0.0.1:8000/admin/")
        title = self.browser.find_elements_by_tag_name('h1')[1]
        self.assertEqual(title.text, "Welcome to EPIC EVENTS")
        logout_button = self.browser.find_elements(By.TAG_NAME, 'a')[1]
        self.assertEqual(logout_button.text, 'logout')

    def test_admin_authentification_user_no_admin(self):
        self.browser.get("http://127.0.0.1:8000/admin/login/")
        form_username = self.browser.find_element_by_id("id_username")
        form_username.send_keys("fred")
        form_password = self.browser.find_element_by_id("id_password")
        form_password.send_keys("fred1234")
        form_password.send_keys(Keys.RETURN)
        self.assertEqual(self.browser.current_url, "http://127.0.0.1:8000/admin/login/")
        error_message = self.browser.find_element_by_class_name("errornote")
        self.assertEqual(error_message.text , "Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.")

    def test_add_user_from_admin(self):
        self.browser.get("http://127.0.0.1:8000/admin/login/")
        form_username = self.browser.find_element_by_id("id_username")
        form_username.send_keys("aurel")
        form_password = self.browser.find_element_by_id("id_password")
        form_password.send_keys("a20081113b")
        form_password.send_keys(Keys.RETURN)
        add_link = self.browser.find_elements_by_class_name("addlink")
        user_add_link = add_link[5]
        user_add_link.send_keys(Keys.RETURN)
        input_username = self.browser.find_element_by_name("username")
        input_username.send_keys("test_username")
        input_password = self.browser.find_element_by_name("password")
        input_password.send_keys("test_pswd")
        input_first_name = self.browser.find_element_by_name("first_name")
        input_first_name.send_keys("test_first_name")
        input_last_name = self.browser.find_element_by_name("last_name")
        input_last_name.send_keys("test_last_name")
        input_email = self.browser.find_element_by_name("email")
        input_email.send_keys("test_email@test.com")
        select_group = self.browser.find_element(By.TAG_NAME, 'option')
        select_group.click()
        select_perm = self.browser.find_element(By.XPATH, "//option[@value='33']")
        select_perm.click()
        select = self.browser.find_element(By.ID, 'id_role') # <select name="role" required="" id="id_role">
        select.send_keys(Keys.ARROW_DOWN)
        select.send_keys(Keys.RETURN) # <option value="2">manager</option>  
        time.sleep(10)    
        submit_button = self.browser.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()
        time.sleep(10)
        accueil_user = self.browser.find_element(By.ID, 'content') #<div id="content" class=""> <h1>Select user to change</h1>
        assert "Change user" in accueil_user.text
        new_user = self.browser.find_element_by_class_name("success")
        print(new_user.text)
        assert "The user “test_username” was added successfully. You may edit it again below." in new_user.text
