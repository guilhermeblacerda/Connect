from django.db import models
from django import forms
from django.contrib.auth.models import User


class Teacher(models.Model):
    nome = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome}"


# Create your models here.
