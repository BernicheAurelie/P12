from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


def test_open_edge():
    driver = webdriver.Edge("tests/fonctionnels/msedgedriver.exe")
    driver.get('https://www.google.fr/')
    driver.quit()


def test_open_chrome():
    driver = webdriver.Chrome("tests/fonctionnels/chromedriver.exe")
    driver.get('https://www.google.fr/')
    driver.quit()


class TestSetUp(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome("tests/fonctionnels/chromedriver.exe")

    def tearDown(self):
        self.browser.close()
