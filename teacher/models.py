from django.db import models
from django import forms
from student.models import Serie,Materia
from django.contrib.auth.models import User


class Teacher(models.Model):
    nome = models.OneToOneField(User, on_delete=models.CASCADE)
    materia = models.ManyToManyField(Materia)
    serie = models.ManyToManyField(Serie)

    @classmethod
    def criar(cls,nome,materia,serie):
        teacher = cls.objects.create(
            nome=nome
        )

        teacher.materia.set(materia)
        teacher.serie.set(serie)

        return teacher

    def __str__(self):
        return f"{self.nome}"


# Create your models here.
