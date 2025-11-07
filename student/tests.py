from django.test import TestCase,override_settings
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from django.contrib.auth.models import User
import time

from .models import *

@override_settings(DEBUG=True)
class TesteE2EStudent(LiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')        
        options.add_argument("--disable-infobars")
        options.add_argument("--incognito")

        service = Service(ChromeDriverManager().install())
        cls.browser = webdriver.Chrome(service=service, options=options)
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):  
        super().tearDownClass()

    def Login(self):
        self.browser.delete_all_cookies()

        usuario = User.objects.filter(username="teste").first()

        if usuario is None:
            usuario = User.objects.create_user(username="teste",password="123456")

        self.browser.get(f'{self.live_server_url}/')

        self.assertIn('Login',self.browser.page_source)

        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')

        username_input.send_keys('teste')
        password_input.send_keys('123456')
        password_input.send_keys(Keys.RETURN)

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"connect"))
        )

        self.assertIn('CONNECT',self.browser.page_source)

        return usuario
    

    def test_1_Boletim(self):

        usuario = self.Login()

        boleto = Boleto.objects.create(usuario=usuario,dataDeVencimento="2025-11-10",valor=1000.0)
        Boleto.objects.create(usuario=usuario,dataDeVencimento="2025-11-25",valor=1000.0,pago=True)

        button = self.browser.find_element(By.TAG_NAME,"button")
        button.click()

        link = self.browser.find_element(By.NAME, "boletos")
        link.click()

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"boletosInfo"))
        )

        link = self.browser.find_element(By.NAME,f"{boleto.id}")
        link.click()

        WebDriverWait(self.browser, 10).until(
            expected_conditions.url_contains("pdf")
        )

    def test_2_RegisterLogin(self):
        self.browser.delete_all_cookies()

        self.browser.get(f'{self.live_server_url}/register/')

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"register"))
        )
        
        username_input = self.browser.find_element(By.NAME, 'username')
        email_input = self.browser.find_element(By.NAME,"email")
        password_input = self.browser.find_element(By.NAME, 'password')

        username_input.send_keys('teste')
        email_input.send_keys('teste@gmail.com')
        password_input.send_keys('123456')
        password_input.send_keys(Keys.RETURN)

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"login"))
        )

        self.assertIn('Login',self.browser.page_source)

        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')

        username_input.send_keys('teste')
        password_input.send_keys('123456')
        password_input.send_keys(Keys.RETURN)

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"connect"))
        )

        self.assertIn('CONNECT',self.browser.page_source)

