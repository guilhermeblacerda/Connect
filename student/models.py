from django.db import models
from django.contrib.auth.models import User
from datetime import date
from multiselectfield import MultiSelectField

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
    dias = MultiSelectField(choices=Dias_semana,blank=True, default=list)

    @classmethod
    def criar(cls,nome,dias):
        materia = cls.objects.create(
            nome = nome,
            dias = dias
        )
        materia.save()

        return materia

    def get_dias(self):
        lista = []

        for n in self.dias:
            lista.append(int(n))

        return lista

    def __str__(self):
        return f"{self.nome}"
    
class Serie(models.Model):
    nome = models.CharField(max_length=50)
    materia = models.ManyToManyField(Materia,null=True)

    @classmethod
    def criar(cls,nome,materia):
        serie = cls.objects.create(nome=nome)
        serie.materia.add(materia)

        return serie

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    serie = models.ForeignKey(Serie,on_delete=models.CASCADE)
    materias = models.ManyToManyField(Materia,related_name='alunos')

    @classmethod
    def criar(cls,user,serie,materia):
        aluno = cls.objects.create(
            user = user,
            serie = serie,
        )

        aluno.materias.set(materia)

        return aluno    

    def __str__(self):
        return f"{self.user} - {self.serie.nome}"
    
class Media(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='medias')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='medias')
    valor = models.FloatField()

    @classmethod
    def criar(cls,aluno,materia,valor):
        return cls.objects.create(
            aluno = aluno,
            materia = materia,
            valor = valor
        )

    def __str__(self):
            return f"{self.aluno.user.username} - {self.materia.nome}: {self.valor}"

    
class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno,on_delete=models.CASCADE,related_name='avaliacoes')
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
    
class Boleto(models.Model):
    usuario = models.ForeignKey(User, related_name="boletos",on_delete=models.CASCADE)
    dataDeVencimento = models.DateTimeField()
    valor = models.FloatField()
    link = models.URLField(blank=True,null=True)
    pago = models.BooleanField(default=False, verbose_name='Pago')
    dataDePagamento = models.DateField(blank=True,null=True,verbose_name="Data De Pagamento")

    criadoEm = models.DateTimeField(auto_now_add=True)
    atualizadoEm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Boleto{self.id} - {self.usuario.username} - R$ {self.valor:.2f}"
    
    @property
    def EstaVencida(self):
        return (not self.pago) and (self.dataDeVencimento < date.today())

# Create your models here.
