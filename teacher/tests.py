from django.test import TestCase
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from django.contrib.auth.models import User
import time

from student.models import Serie,Materia,Aluno
from .models import *

class LoginE2ETeste(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()


    @classmethod
    def tearDownClass(cls):  
        super().tearDownClass()

    def loginAsTeacher(self):

        user = User.objects.filter(username='teste').first()

        if user is None:
            user = User.objects.create_user(username = 'teste',password = '123456')

        self.browser.get(f'{self.live_server_url}/teacher/login/')

        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')

        username_input.send_keys('teste')
        password_input.send_keys('123456')
        password_input.send_keys(Keys.RETURN)

        self.assertIn('Login',self.browser.page_source)

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"connect"))
        )   

        return user
    
    def test_RecordAbsence(self):

        user = User.objects.create_user(username='teste', password='123456')

        materia = Materia.criar('matematica', ['1'])

        serie = Serie.criar('1º ano',materia)

        professor = Teacher.criar(user, [materia], [serie])

        aluno_user = User.objects.create_user(username='alunoteste', password='teste123')

        aluno = Aluno.criar(aluno_user,serie,[materia])

        self.loginAsTeacher()

        button = self.browser.find_element(By.TAG_NAME,"button")
        button.click()

        link = self.browser.find_element(By.NAME, "absence")
        link.click()

        link = self.browser.find_element(By.NAME, f"{self.materia.nome}{self.serie.nome}")
        link.click()




# Create your tests here.