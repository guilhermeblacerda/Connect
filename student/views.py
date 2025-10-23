from django.shortcuts import render,redirect

from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.db.models import Count,Q
from .models import Falta,Avaliacao,Aluno,Materia,Mensagem,Media
import json

def home_page(request):
    return render(request,"student/home.html")

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
 
    return render(request, "student/login.html", context)

def register_page(request):
    context = {}

    if request.method == "POST":
        name = request.POST.get('username')
        email = request.POST.get('email')
        passw = request.POST.get('password')

        if not name or not email or not passw:
            context['error'] = 'Preencha todos os campos'
            
            return render(request, 'student/register.html',context)
        
        if User.objects.filter(username=name).exists():
            context['error'] = 'Usuario ja existe'

            return render(request, 'student/register.html',context)
        
        user = User.objects.create_user(username=name,email=email,password=passw)
        return redirect('login')

    return render(request, 'student/register.html',context)

def logout_page(request):
    logout(request)
    return(redirect('login'))


def absence_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    faltas = Falta.objects.filter(aluno__user=request.user).order_by('-data')
    total = faltas.count()
    return render(request, 'student/absence.html',{'faltas': faltas, 'total': total})

def score_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    aluno = Aluno.objects.filter(user=request.user).first()

    if aluno:
        materias = aluno.materias.all()
        avaliacoes = Avaliacao.objects.filter(aluno__user=request.user).order_by('-data')
        medias = aluno.medias.all()

        return render(request, 'student/score.html',{'materias': materias,'avaliacoes': avaliacoes,'aluno':aluno,'medias':medias})

    return render(request, 'student/score.html')

def calendar_page(request):
    if not request.user.is_authenticated:
        return redirect('login')

    aluno = Aluno.objects.filter(user=request.user).first()

    if aluno:
        materias = aluno.materias.all()

        eventos = []    

        for materia in materias:
            eventos.append({
                "title":materia.nome,
                "daysOfWeek": materia.get_dias(),
            })

        return render(request,'student/calendar.html',{'materias': materias,'eventos': json.dumps(eventos)})

    return render(request,'student/calendar.html')

def chat_page(request,usuario_id=None):
    user = request.user
    mensagens = []
    destinatario = None

    if user.is_staff:
        usuarios = User.objects.exclude(is_staff=True)
        usuarios = usuarios.annotate(
            toRead = Count('mensagens_enviadas',filter=Q(mensagens_enviadas__destinatario=user,mensagens_enviadas__lida=False))
        )
    else:
        usuarios = None
        usuario_id = User.objects.get(username="stackadmin").id

    if usuario_id:
        destinatario = User.objects.get(id=usuario_id)

        Mensagem.objects.filter(
            remetente__in=[user,destinatario],
            destinatario__in=[user, destinatario]
        ).update(lida=True)

        mensagens = Mensagem.objects.filter(
            remetente__in=[user,destinatario],
            destinatario__in=[user, destinatario]
        ).order_by('data_envio','id')

    if request.method == 'POST':
        documentos = request.POST.get("documentos")
        dispensa = request.POST.get("dispensa")
        texto = request.POST.get('mensagem')

        if destinatario:
            if documentos:
                Mensagem.objects.create(remetente=user,destinatario=destinatario,texto=documentos)
            elif dispensa:
                Mensagem.objects.create(remetente=user,destinatario=destinatario,texto=dispensa)
            elif texto:
                Mensagem.objects.create(remetente=user,destinatario=destinatario,texto=texto) 
            
            return redirect('chat', usuario_id=destinatario.id)
        
    return render(request,'student/chat.html', {'mensagens': mensagens,'destinatario':destinatario, 'usuarios':usuarios})

# Create your views here.