from django.test import TestCase
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from django.contrib.auth.models import User
import time
from .models import *

import time

class LoginE2ETeste(LiveServerTestCase):

    def criar_driver():
        """Criar novo WebDriver"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        return driver

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.headless = True
        cls.browser = cls.criar_driver()

    @classmethod
    def tearDownClass(cls):  
        super().tearDownClass()


    def login(self):

        user = User.objects.filter(username='teste').first()

        if user is None:
            user = User.objects.create_user(username = 'teste',password = '123456')

        self.browser.get(f'{self.live_server_url}/')

        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')

        username_input.send_keys('teste')
        password_input.send_keys('123456')
        password_input.send_keys(Keys.RETURN)

        self.assertIn('Login',self.browser.page_source)

        WebDriverWait(self.browser, 10).until(
            expected_conditions.url_contains("home")
        )   

        return user
    
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

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"login"))
        )

        self.login()

        self.assertIn('CONNECT',self.browser.page_source)

    def test_absences(self):

        user = self.login()

        serie = Serie.criar("1º",None)

        materia = Materia.criar("Teste",["0"])

        aluno = Aluno.criar(user,serie,[materia])

        falta = Falta.criar(aluno,materia,'2025-10-20',False,"-")

        button = self.browser.find_element(By.TAG_NAME,"button")
        button.click()

        link = self.browser.find_element(By.NAME, "absence")
        link.click()

        time.sleep(1)

    def test_score(self):

        user = self.login()

        serie = Serie.criar("1º",None)

        materia = Materia.criar("Teste",["0"])

        aluno = Aluno.criar(user,serie,[materia])

        avaliacao = Avaliacao.criar(aluno,materia,1,10,"2025-10-31")

        button = self.browser.find_element(By.TAG_NAME,"button")
        button.click()

        link = self.browser.find_element(By.NAME, "score")
        link.click()

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"score"))
        )

        time.sleep(1)

        button = self.browser.find_element(By.NAME, "Teste")
        self.browser.execute_script("arguments[0].click();", button)

        time.sleep(1)

    def test_calendar(self):

        user = self.login()

        serie = Serie.criar("1º",None)

        materia = Materia.criar("Teste",["0"])

        aluno = Aluno.criar(user,serie,[materia])

        button = self.browser.find_element(By.TAG_NAME,"button")
        button.click()

        time.sleep(1)

        link = self.browser.find_element(By.NAME, "calendar")
        link.click()

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"calendar"))
        )

        self.browser.execute_script("window.scrollBy(0, 150);")


# Create your tests here.
