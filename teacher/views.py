from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from student.models import Serie,Materia,Aluno,Falta,Avaliacao,Media
from django.utils import timezone
from django.utils.text import slugify
from .models import Teacher

'''
    Função que gera um nome unico para cada usuario,
    recebendo o nome base, ele altera o nome do usuario de acordo
    com o numero de usuarios com aquele determinado node
'''
def GenerateUniqueUsername(nomeBase):
    nomeBase = slugify(nomeBase)
    nomeDoUsuario = nomeBase
    i = 1

    while User.objects.filter(username=nomeDoUsuario).exists():
        nomeDoUsuario = f"{nomeBase}{i}"
        i += 1

    return nomeDoUsuario

'''
    Função que manda o usuario para o login 
'''
def GoToLogin(request):
    
    context = {} #Dicionario que passado para o frontend 

    if request.method == 'POST': #checa se o tipo de requerimento é de envio
        nomeDoUsuario = request.POST.get('username')
        senhaDoUsuario = request.POST.get('password')

        user = authenticate(request,username=nomeDoUsuario,password=senhaDoUsuario) ##função que pega o usuario associado ao login e senha do usuario

        if user is not None and hasattr(user,'teacher'): ##parte que checa se o usuario foi encontrado
            login(request, user) ##loga o usuario

            return redirect('teacherHome') ##redireciona para o home
        else:
            context['error'] = "Professor não encontrado" ##define o valor de error dentro do dicionario context

    return render(request, "teacher/login.html",context) ##renderiza a pagina
    
'''
    Manda o usuario para o home
'''
def GoToHome(request):
    return render(request, "teacher/home.html")

'''
    Função que manda o usuario para a pagina de faltas
'''
def GoToAbsence(request,serieId = None,materiaId = None):
    if not request.user.is_authenticated: ##checa se o usuario esta logado
        return redirect('teacherLogin') ##Se não estiver logado redireciona para o login
    
    usuario = request.user
    professor = Teacher.objects.filter(nome = usuario).first() ##pega um professor de acordo com o usuario logado

    if not professor: ##checa se existe um professor
        return redirect('teacherLogin')
    
    context = {}
    materias_series = []
    alunos = []
    selected = False

    series = professor.serie.all()

    for serie in series:
        materias = serie.materia.filter(id__in=professor.materia.values_list('id', flat=True))

        for materia in materias:
            materias_series.append((materia, serie))
            context['materias_series'] = materias_series 

    if serieId and materiaId:
        selected = True

        serie = Serie.objects.get(id=serieId)
        materia = Materia.objects.get(id=materiaId)
        alunos = Aluno.objects.filter(
            serie=serie,
            materias__id=materia.id
        )

    if request.method == "POST":
        ausentesIds = request.POST.getlist('ausentes')

        serie = Serie.objects.get(id=serieId)
        materia = Materia.objects.get(id=materiaId)
        alunos = Aluno.objects.filter(serie=serie,materias=materia)

        for aluno in alunos:
            if str(aluno.id) in ausentesIds:
                Falta.criar(
                    aluno = aluno,
                    materia=materia,
                    data=timezone.now().date(),
                    justificada=False,
                    comentario='-',
                )

        return redirect('teacherAbsence')

    context['alunos'] = alunos
    context['selected'] = selected

    return render(request,"teacher/absence.html",context)

'''
    Função para ir para a pagina de notas
'''
def GoToScore(request,serieId=None,materiaId=None,alunoId=None):
    if not request.user.is_authenticated: ##Checa se o usuario esta autenticado
        return redirect('teacherLogin')

    usuario = request.user
    professor = Teacher.objects.filter(nome = usuario).first()

    if not professor:
        return redirect('teacherLogin')

    context = {}
    aluno = []
    materias_series = []
    selectedGrade = []
    selectedStudent = False

    series = professor.serie.all()

    for serie in series:
        materias = serie.materia.filter(id__in=professor.materia.values_list('id', flat=True))

        for materia in materias:
            materias_series.append((materia, serie))
            context['materias_series'] = materias_series

    if serieId and materiaId:
        selectedGrade = [Serie.objects.get(id=serieId),Materia.objects.get(id=materiaId)]

        serie = Serie.objects.get(id=serieId)
        materia = Materia.objects.get(id=materiaId)
        aluno = Aluno.objects.filter( 
            serie=serie,
            materias=materia
        )
        
        if alunoId:
            selectedStudent = True
            
            aluno = Aluno.objects.get(id=alunoId)
            materias_series = [(Materia.objects.get(id=materiaId),Serie.objects.get(id=serieId))]

        if request.method == "POST":
            avaliacaoButton = request.POST.get('avaliacaoButton')
            mediaButton = request.POST.get('mediaButton')
            adicionarButton = request.POST.get('adicionarButton')

            if adicionarButton and not alunoId:
                nome = request.POST.get("nome")

                if nome:
                    username = GenerateUniqueUsername(nome)
                    aluno_user = User.objects.create_user(username=username, password="senha_padrao123")

                    aluno = Aluno.criar(
                        aluno_user,
                        serie,
                        [materia]
                    )

                    return redirect('teacherScoreDetail', serieId=serie.id, materiaId=materia.id)

            if avaliacaoButton:
                nota = request.POST.get("nota")
                data = request.POST.get("data")

                num_avaliacoes = Avaliacao.objects.filter(aluno=aluno, materia=materia).count() + 1

                Avaliacao.criar(
                    aluno,
                    Materia.objects.get(id=materiaId),
                    num_avaliacoes,
                    nota,
                    data
                )

                return redirect('teacherScoreDetail', serieId=serie.id, materiaId=materia.id)

            if mediaButton:
                media = request.POST.get("media")

                Media.criar(
                    aluno,
                    Materia.objects.get(id=materiaId),
                    media
                )
                
                return redirect('teacherScoreDetail', serieId=serie.id, materiaId=materia.id)

    context['alunos'] = aluno
    context['selectedGrade'] = selectedGrade
    context['selectedStudent'] = selectedStudent

    return render(request,"teacher/score.html",context)

# Create your views here.
