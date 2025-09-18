from django.shortcuts import render,redirect

from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from .models import Falta

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
    if request.method == "POST":
        name = request.POST.get('username')
        email = request.POST.get('email')
        passw = request.POST.get('password')

        if not name:
            return redirect('register')
        
        if User.objects.filter(username=name).exists():
            return redirect('register')
        
        user = User.objects.create_user(username=name,email=email,password=passw)
        return redirect('login')

    return render(request, 'forum/register.html')

def logout_page(request):
    logout(request)
    return(redirect('login'))


def absence_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    faltas = Falta.objects.filter(user=request.user).order_by('-data')
    total = faltas.count()
    return render(request, 'forum/absence.html',{'faltas': faltas, 'total': total})

def score_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'forum/score.html')

# Create your views here.