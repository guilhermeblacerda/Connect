from django.shortcuts import render,redirect

from django.contrib.auth import login,authenticate
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

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


def absence_page(request):
    return render(request, 'forum/absence.html')

# Create your views here.