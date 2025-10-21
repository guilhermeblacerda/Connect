from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

class Serie(models.Model):
    nome = models.CharField(max_length=50)

    @classmethod
    def criar(cls,nome):
        return cls.objects.create(nome=nome)

    def __str__(self):
        return self.nome

class Materia(models.Model):
    Dias_semana = (
        ('0','Domingo'),
        ('1','Segunda_feira'),
        ('2','Terça_feira'),
        ('3','Quarta_feira'),
        ('4','Quinta_feira'),
        ('5','Sexta_feira'),
        ('6','Sabado'),
    )

    nome = models.CharField(max_length=50)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    dias = MultiSelectField(choices=Dias_semana,blank=True, default=list)

    @classmethod
    def criar(cls,nome,serie,dias):
        return cls.objects.create(
            nome = nome,
            serie = serie,
            dias = dias
        )

    def get_dias(self):
        lista = []

        for n in self.dias:
            lista.append(int(n))

        return lista

    def __str__(self):
        return f"{self.nome} - {self.serie.nome}"
    
class Aluno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    serie = models.ForeignKey(Serie,on_delete=models.CASCADE)
    materias = models.ManyToManyField(Materia,related_name='alunos')

    @classmethod
    def criar(cls,user,serie,materias):
        aluno = cls.objects.create(
            user = user,
            serie = serie,
        )

        aluno.materias.set(materias)

        return aluno    

    def __str__(self):
        return f"{self.user} - {self.serie.nome}"
    
class Nota(models.Model):
    aluno = models.ForeignKey(Aluno,on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia,on_delete=models.CASCADE)
    serie = models.ForeignKey(Serie,on_delete=models.CASCADE)
    media = models.FloatField()
    data = models.DateField()

    @classmethod
    def criar(cls,aluno,materia,serie,media,data):
        return cls.objects.create(
            aluno = aluno,
            materia = materia,
            serie = serie,
            media = media,
            data = data
        )

    def __str__(self):
        return f"{self.materia.nome} - {self.aluno} {self.serie} - {self.data}"
    
class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno,on_delete=models.CASCADE,related_name='aluno')
    materia = models.ForeignKey(Materia,on_delete=models.CASCADE)
    numero = models.IntegerField() 
    nota = models.FloatField()
    data = models.DateField()

    @classmethod
    def criar(cls,aluno,materia,numero,nota,data):
        return cls.objects.create(
            aluno = aluno,
            materia = materia,
            numero = numero,
            nota = nota,
            data = data
        )
        

    def __str__(self):
        return f"avaliação {self.numero} de {self.materia} - {self.aluno.user} - {self.data}"
    
class Falta(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    data = models.DateField()
    justificada = models.BooleanField(default=False)
    comentario = models.TextField(blank=True,default="-")

    @classmethod
    def criar(cls,aluno,materia,data,justificada,comentario):
        return cls.objects.create(
            aluno = aluno,
            materia = materia,
            data = data,
            justificada = justificada,
            comentario = comentario
        )

    def __str__(self):
        return f"{self.materia.nome} - {self.data} - {str(self.aluno.user)}"
    
class Mensagem(models.Model):
    remetente = models.ForeignKey(User, related_name='mensagens_enviadas',on_delete=models.CASCADE)
    destinatario = models.ForeignKey(User, related_name='mensagens_recebidas',on_delete=models.CASCADE)
    texto = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.remetente} -> {self.destinatario}: {self.texto[:20]}"
    
# Create your models here.
