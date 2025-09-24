from django.shortcuts import render,redirect

from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from .models import Falta,Nota,Avaliacao,Aluno,Materia
import json

def home_page(request):
    return render(request,"forum/home.html")

def login_page(request):
    context = {}

    if request.method == 'POST':
        name = request.POST.get('username')
        passw = request.POST.get('password')

        user = authenticate(request, username=name, password=passw)

        if user is not None:
            login(request, user)

            return redirect ('home')
        else:
            context['error'] = 'Nome de usuario ou senha incorretos'
 
    return render(request, "forum/login.html", context)

def register_page(request):
    context = {}

    if request.method == "POST":
        name = request.POST.get('username')
        email = request.POST.get('email')
        passw = request.POST.get('password')

        if not name or not email or not passw:
            context['error'] = 'Preencha todos os campos'
            
            return render(request, 'forum/register.html',context)
        
        if User.objects.filter(username=name).exists():
            context['error'] = 'Usuario ja existe'

            return render(request, 'forum/register.html',context)
        
        user = User.objects.create_user(username=name,email=email,password=passw)
        return redirect('login')

    return render(request, 'forum/register.html',context)

def logout_page(request):
    logout(request)
    return(redirect('login'))


def absence_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    faltas = Falta.objects.filter(aluno__user=request.user).order_by('-data')
    total = faltas.count()
    return render(request, 'forum/absence.html',{'faltas': faltas, 'total': total})

def score_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    aluno = Aluno.objects.filter(user=request.user).first()

    if aluno:
        materias = Materia.objects.filter(serie=aluno.serie)
        avaliacoes = Avaliacao.objects.filter(aluno__user=request.user).order_by('-data')

        return render(request, 'forum/score.html',{'materias': materias,'avaliacoes': avaliacoes})

    return render(request, 'forum/score.html')

def calendar_page(request):
    if not request.user.is_authenticated:
        return redirect('login')

    aluno = Aluno.objects.filter(user=request.user).first()
    materias = Materia.objects.filter(serie=aluno.serie)

    eventos = []    

    for materia in materias:
        eventos.append({
            "title":materia.nome,
            "daysOfWeek": materia.get_dias(),
        })


    return render(request,'forum/calendar.html',{'materias': materias,'eventos': json.dumps(eventos)})

# Create your views here.