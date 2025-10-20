from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User

import time

class LoginE2ETeste(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_register_login(self):

        self.browser.get(f'{self.live_server_url}/register/') 

        self.assertIn('Register',self.browser.page_source)

        username_input = self.browser.find_element(By.NAME, 'username')
        email_input = self.browser.find_element(By.NAME,'email')
        password_input = self.browser.find_element(By.NAME, 'password')

        username_input.send_keys('teste')
        email_input.send_keys('a@gmail.com')
        password_input.send_keys('123456')
        password_input.send_keys(Keys.RETURN)

        time.sleep(5)

        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')

        username_input.send_keys('teste')
        password_input.send_keys('123456')
        password_input.send_keys(Keys.RETURN)

        self.assertIn('Login',self.browser.page_source)

        time.sleep(5)   

        self.assertIn('CONNECT',self.browser.page_source)
      

# Create your tests here.
