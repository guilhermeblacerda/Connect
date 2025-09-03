from django.shortcuts import render

def home_page(request):
    return render(request,"forum/home.html")

def login_page(request):
    return render(request, "forum/login.html")

# Create your views here.