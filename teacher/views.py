from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
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


# Create your views here.
