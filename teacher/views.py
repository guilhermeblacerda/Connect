from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from student.models import Serie,Materia,Aluno,Falta,Avaliacao,Media
from django.utils import timezone
from .models import Teacher

def GoToLogin(request):
    context = {}

    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=name,password=password)

        if user is not None and hasattr(user,'teacher'):
            login(request, user)

            return redirect('teacherHome')
        else:
            context['error'] = "Professor não encontrado" 

    return render(request, "teacher/login.html",context)
    
def GoToHome(request):
    return render(request, "teacher/home.html")

def GoToClass(request):

    user = request.user

    if user is None:
        return redirect("teacherLogin")

    professor = Teacher.objects.get(nome=user)

    if request.method == 'POST':
        nome = request.POST.get('nome')

        serie = Serie.criar(nome)

    professor.serie.add(serie)

    turmas = professor.serie.all()

    return render(request, "teacher/class.html")

def GoToAbsence(request,serieId = None,materiaId = None):
    if not request.user.is_authenticated:
        return redirect('teacherLogin')
    
    user = request.user
    professor = Teacher.objects.filter(nome = user).first()

    if not professor:
        return redirect('teacherLogin')
    
    alunos = []
    series = []
    materias_series = []
    selected = False

    series = professor.serie.all()

    for serie in series:
        materias = serie.materia.filter(id__in=professor.materia.values_list('id', flat=True))
        for materia in materias:
            materias_series.append((materia, serie))

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

    return render(request,"teacher/absence.html",{'materias_series':materias_series,'alunos':alunos,'selected':selected})

def GoToScore(request,serieId=None,materiaId=None,alunoId=None):
    if not request.user.is_authenticated:
        return redirect('teacherLogin')

    user = request.user
    professor = Teacher.objects.filter(nome = user).first()

    if not professor:
        return redirect('teacherLogin')

    alunos = []
    series = []
    materias_series = []
    selectedGrade = False
    selectedStudent = False

    series = professor.serie.all()

    for serie in series:
        materias = serie.materia.filter(id__in=professor.materia.values_list('id', flat=True))
        for materia in materias:
            materias_series.append((materia, serie))

    if serieId and materiaId:
        selectedGrade = True
        serie = Serie.objects.get(id=serieId)
        materia = Materia.objects.get(id=materiaId)
        alunos = Aluno.objects.filter( 
            serie=serie,
            materias=materia
        )
        
        if alunoId:
            selectedStudent = True
            alunos = Aluno.objects.get(id=alunoId)
            materias_series = [(Materia.objects.get(id=materiaId),Serie.objects.get(id=serieId))]

    if request.method == "POST":
        avaliacaoButton = request.POST.get('avaliacaoButton')
        mediaButton = request.POST.get('mediaButton')

        if avaliacaoButton:
            nota = request.POST.get("nota")
            data = request.POST.get("data")

            Avaliacao.criar(
                alunos,
                Materia.objects.get(id=materiaId),
                Avaliacao.objects.filter(aluno=alunos, materia=materia).count()+1,
                nota,
                data
            )

        if mediaButton:
            media = request.POST.get("media")

            Media.criar(
                alunos,
                Materia.objects.get(id=materiaId),
                media
            )
            
        return redirect('teacherScore')


    return render(request,"teacher/score.html",{
        'materias_series':materias_series,
        'alunos':alunos,
        'selectedGrade':selectedGrade,
        'selectedStudent':selectedStudent,
        })

# Create your views here.
