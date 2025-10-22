from django.test import TestCase,override_settings
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from django.contrib.auth.models import User
import time

from student.models import Serie,Materia,Aluno,Avaliacao,Media
from student.tests import *
from .models import *

@override_settings(DEBUG=True, ALLOWED_HOSTS=['*'])
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

    def test_RegisterStudent(self):

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

        print("ESPERANDO ABRIR A PAGINA DE ESTUDANTES ")
        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"ScoreGuideStudents"))
        )

        print("PROCURANDO ENTRY PARA NOME")
        username_input = self.browser.find_element(By.NAME, 'nome')
        username_input.send_keys('alunoteste')
        username_input.send_keys(Keys.RETURN)

        time.sleep(1)

        print("ESPERANDO ABRIR A PAGINA DE ESTUDANTES ")
        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"ScoreGuideStudents"))
        )        

        username_input = self.browser.find_element(By.NAME, 'nome')
        username_input.clear()
        username_input.send_keys('alunoteste')
        username_input.send_keys(Keys.RETURN)

        time.sleep(1)

        alunos = User.objects.filter(username__startswith='alunoteste')
        self.assertEqual(alunos.count(), 2)
        self.assertTrue(User.objects.filter(username='alunoteste').exists())
        self.assertTrue(User.objects.filter(username='alunoteste1').exists())

    def test_CadastrarNota(self):
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

        print("ESPERANDO ABRIR A PAGINA DE ESTUDANTES ")
        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"ScoreGuideStudents"))
        )        

        link = self.browser.find_element(By.NAME, f"{aluno.user}")
        link.click()

        nota_input = self.browser.find_element(By.NAME, 'nota')
        data_input = self.browser.find_element(By.NAME, 'data')

        nota_input.send_keys(10)
        data_input.send_keys('2025-10-22')
        time.sleep(1)
        nota_input.send_keys(Keys.RETURN)
        print("Enviou a avaliação")
        
        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.NAME,"ScoreGuideStudents"))
        )   
        print("ABRIU A LISTA DE ALUNOS")

        link = self.browser.find_element(By.NAME, f"{aluno.user}")
        link.click()

        media_input = self.browser.find_element(By.NAME, 'media')
        media_input.send_keys(10)
        media_input.send_keys(Keys.RETURN)

        time.sleep(1)

        media = aluno.medias.all().first()
        self.assertEqual(media.valor, 10)

    def test_enviarMensagemParaDiretoria(self):

        admin = User.objects.create_superuser(username="stackadmin",password="123")

        admin.id = 1

        user = User.objects.create_user(username='teste', password='123456')

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

        button = self.browser.find_element(By.TAG_NAME,"button")
        button.click()

        time.sleep(3)

        link = self.browser.find_element(By.NAME, "chat")
        link.click()

        time.sleep(1)

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID,"chatArea"))
        )

        text_input = self.browser.find_element(By.NAME,'mensagem')
        text_input.send_keys('teste')
        time.sleep(1)
        text_input.send_keys(Keys.RETURN)

        time.sleep(1)        

    def test_SolicitarParaDiretoria(self):

        admin = User.objects.create_superuser(username="stackadmin",password="123")

        admin.id = 1

        user = User.objects.create_user(username='teste', password='123456')

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

        button = self.browser.find_element(By.TAG_NAME,"button")
        button.click()

        time.sleep(3)

        link = self.browser.find_element(By.NAME, "chat")
        link.click()

        time.sleep(1)

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID,"chatArea"))
        )

        solicitar = self.browser.find_element(By.NAME,'documentos')
        solicitar.click()
        dispensa = self.browser.find_element(By.NAME,'dispensa')
        dispensa.click()

        time.sleep(1)      

# Create your tests here.