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

from student.models import Serie,Materia,Aluno,Avaliacao,Media
from student.tests import *
from .models import *

@override_settings(DEBUG=True)
class LoginE2ETeste(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        
        options.add_argument("--disable-infobars")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--incognito")

        service = Service(ChromeDriverManager().install())
        cls.browser = webdriver.Chrome(service=service, options=options)
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):  
        super().tearDownClass()

        ##Função para logar como professor##
    def loginAsTeacher(self):
        self.browser.delete_all_cookies() # limpar os cookies

        user = User.objects.filter(username='teste').first()

        if user is None:
            user = User.objects.create_user(username = 'teste',password = '123456')

        self.browser.get(f'{self.live_server_url}/teacher/login/')

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

        return user
    
    ##Teste de registrar Falta##
    def test_1_RecordAbsence(self):

        self.browser.delete_all_cookies() # limpar os cookies

        ##Criação dos modelos Django##
        user = User.objects.create_user(username='teste', password='123456')
        materia = Materia.criar('matematica', ['1'])
        serie = Serie.criar('1º ano',materia)
        professor = Teacher.criar(user, [materia], [serie])
        aluno_user = User.objects.create_user(username='alunoteste', password='teste123')
        aluno = Aluno.criar(aluno_user,serie,[materia])

        ##logando##
        self.loginAsTeacher()

        button = self.browser.find_element(By.TAG_NAME,"button")
        button.click()

        link = self.browser.find_element(By.NAME, "absence")
        link.click()

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID,"absenceGuide"))
        ) 

        link = self.browser.find_element(By.NAME, f"{materia.nome}{serie.nome}")
        link.click()

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"ausentes"))
        ) 

        checkbox = self.browser.find_element(By.NAME, 'ausentes')

        if not checkbox.is_selected():
            checkbox.click()

        button = self.browser.find_element(By.ID,"submitButton")
        button.click()


    ##Teste de cadastrar aluno##
    def test_2_RegisterStudent(self):
        self.browser.delete_all_cookies() # limpar os cookies
        
        ##Criação dos modelos Django##
        user = User.objects.create_user(username='teste', password='123456')
        materia = Materia.criar('matematica', ['1'])
        serie = Serie.criar('1º ano',materia)
        professor = Teacher.criar(user, [materia], [serie])

        self.loginAsTeacher()

        button = self.browser.find_element(By.TAG_NAME,"button")
        button.click()

        link = self.browser.find_element(By.NAME, "score")
        link.click()

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"ScoreGuide"))
        ) 

        link = self.browser.find_element(By.NAME, f"{materia.nome}{serie.nome}")
        link.click()

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"ScoreGuideStudents"))
        )

        username_input = self.browser.find_element(By.NAME, 'nome')
        username_input.send_keys('alunoteste')
        username_input.send_keys(Keys.RETURN)

        time.sleep(1)

        username_input = self.browser.find_element(By.NAME, 'nome')
        username_input.clear()
        username_input.send_keys('alunoteste')
        username_input.send_keys(Keys.RETURN)

        alunos = User.objects.filter(username__startswith='alunoteste')
        self.assertEqual(alunos.count(), 2)
        self.assertTrue(User.objects.filter(username='alunoteste').exists())
        self.assertTrue(User.objects.filter(username='alunoteste1').exists())


    ##Teste de cadastro de nota##
    def test_3_CadastrarNota(self):

        self.browser.delete_all_cookies() # limpar os cookies

        ##Criando os modelos Django##
        user = User.objects.create_user(username='teste', password='123456')
        materia = Materia.criar('matematica', ['1'])
        serie = Serie.criar('1º ano',materia)
        professor = Teacher.criar(user, [materia], [serie])
        aluno_user = User.objects.create_user(username='alunoteste', password='teste123')
        aluno = Aluno.criar(aluno_user,serie,[materia])

        self.loginAsTeacher()

        button = self.browser.find_element(By.TAG_NAME,"button")
        button.click()

        link = self.browser.find_element(By.NAME, "score")
        link.click()

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"ScoreGuide"))
        ) 

        link = self.browser.find_element(By.NAME, f"{materia.nome}{serie.nome}")
        link.click()

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"ScoreGuideStudents"))
        )        

        link = self.browser.find_element(By.NAME, f"{aluno.user}")
        link.click()

        nota_input = self.browser.find_element(By.NAME, 'nota')
        data_input = self.browser.find_element(By.NAME, 'data')

        nota_input.send_keys(10)
        data_input.clear()
        self.browser.execute_script("arguments[0].value = '2025-10-22';", data_input)
        nota_input.send_keys(Keys.RETURN)

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"ScoreGuideStudents"))
        )   

        link = self.browser.find_element(By.NAME, f"{aluno.user}")
        link.click()

        media_input = self.browser.find_element(By.NAME, 'media')
        media_input.send_keys(10)
        media_input.send_keys(Keys.RETURN)

        time.sleep(1)

        media = aluno.medias.all().first()
        self.assertEqual(media.valor, 10)


    ##Teste De envio de mensagem a diretoria##
    def test_4_enviarMensagemParaDiretoria(self):

        ##Criando os ususarios##
        admin = User.objects.create_superuser(username="stackadmin",password="123")
        user = User.objects.create_user(username='teste', password='123456')

        self.browser.get(f'{self.live_server_url}/')

        self.assertIn('LOGIN',self.browser.page_source)

        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')

        username_input.send_keys('teste')
        password_input.send_keys('123456')
        password_input.send_keys(Keys.RETURN)

        WebDriverWait(self.browser, 10).until(
            expected_conditions.url_contains("home")
        )

        self.assertIn('CONNECT',self.browser.page_source)

        button = self.browser.find_element(By.TAG_NAME,"button")
        button.click()


        link = self.browser.find_element(By.NAME, "chat")
        link.click()

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID,"chatArea"))
        )

        text_input = self.browser.find_element(By.NAME,'mensagem')
        text_input.send_keys('teste')
        text_input.send_keys(Keys.RETURN)


    ##Teste de Solicitações##
    def test_5_SolicitarParaDiretoria(self):

        admin = User.objects.create_superuser(username="stackadmin",password="123")
        user = User.objects.create_user(username='teste', password='123456')

        self.browser.get(f'{self.live_server_url}/')

        self.assertIn('LOGIN',self.browser.page_source)

        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')

        username_input.send_keys('teste')
        password_input.send_keys('123456')
        password_input.send_keys(Keys.RETURN)

        WebDriverWait(self.browser, 10).until(
            expected_conditions.url_contains("home")
        )

        self.assertIn('CONNECT',self.browser.page_source)        

        button = self.browser.find_element(By.TAG_NAME,"button")
        button.click()

        link = self.browser.find_element(By.NAME, "chat")
        link.click()

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID,"chatArea"))
        )

        solicitar = self.browser.find_element(By.NAME,'documentos')
        solicitar.click()
        time.sleep(1)
        dispensa = self.browser.find_element(By.NAME,'dispensa')
        dispensa.click()
        time.sleep(1)


# Create your tests here.