from django.db import models
from django.contrib.auth.models import User



import datetime
from django.utils import timezone

class Pergunta(models.Model):
    titulo = models.CharField(max_length=200, null= False)
    detalhe = models.TextField(null=False)
    tentativa = models.TextField()
    data_criacao = models.DateTimeField("Criado em ")
    usuario = models.CharField(max_length=200, null=False,default="anônimo")

    def __str__(self):
        return "[" + str(self.id) + "]" + self.titulo
    
    def foi_publicado_recentemente(self):
        return self.data_criacao >= timezone.now() - datetime.timedelta(days=1)
    
    def string_detalhada(self):
        return "id: " + str(self.id) + "; titulo: " + self.titulo + "; detalhe: " + self.detalhe + "tentativa: " + self.tentativa + "; data criação: " + str(self.data_criacao) + "; usuario: " + self.usuario

class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    texto = models.TextField(null=False)
    votos = models.IntegerField(default=0)
    data_criacao = models.DateTimeField("Criado em ")
    usuario = models.CharField(max_length=200, null=False,default="anônimo")

    def __str__(self):
        return "[" + str(self.id) + "]" + self.texto
    
    def foi_publicado_recentemente(self):
        return self.data_criacao >= timezone.now() - datetime.timedelta(days=1)

class Materia(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Falta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    data = models.DateField()
    justificada = models.BooleanField(default=False)
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f"{self.materia.nome} - {self.data} - {str(self.user)}"

# Create your models here.
