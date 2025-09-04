from django.shortcuts import render,redirect

from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User

def home_page(request):
    return render(request,"forum/home.html")

def login_page(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        passw = request.POST.get('password')

        user = authenticate(request, username=name, password=passw)

        if user is not None:
            login(request, user)

            return redirect ('home')

    return render(request, "forum/login.html")

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

# Create your views here.