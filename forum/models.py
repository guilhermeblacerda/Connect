from django.db import models
from django.contrib.auth.models import User

class Materia(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Serie(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return str(self.nome)
    
class Aluno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    materias = models.ManyToManyField(Materia,related_name='alunos')

    def __str__(self):
        return str(self.user)
    
class Nota(models.Model):
    aluno = models.ForeignKey(Aluno,on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia,on_delete=models.CASCADE)
    serie = models.ForeignKey(Serie,on_delete=models.CASCADE)
    media = models.FloatField()
    data = models.DateField()

    def __str__(self):
        return f"{self.materia.nome} - {self.aluno} {self.serie} - {self.data}"
    
class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno,on_delete=models.CASCADE)
    numero = models.IntegerField() 
    materia = models.ForeignKey(Materia,on_delete=models.CASCADE)
    nota = models.FloatField()
    data = models.DateField()

    def __str__(self):
        return f"avaliação {self.numero} de {self.materia} - {self.aluno} - {self.data}"
    
class Falta(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    data = models.DateField()
    justificada = models.BooleanField(default=False)
    comentario = models.TextField(blank=True,default="-")

    def __str__(self):
        return f"{self.materia.nome} - {self.data} - {str(self.aluno.user)}"

# Create your models here.
