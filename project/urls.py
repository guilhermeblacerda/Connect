"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from student import views

urlpatterns = [
    path('', views.login_page, name="login"),

    path('register/',views.register_page, name="register"),

    path('home/', views.home_page, name="home"),

    path('admin/', admin.site.urls, name="admin"),

    path('absence/', views.absence_page, name="absence"),

    path('score/', views.score_page, name="score"),

    path('calendar/', views.calendar_page, name="calendar"),

    path('logout/', views.logout_page, name="logout"),

    path('forgot_passwd/',auth_views.PasswordResetView.as_view(
        template_name = 'student/forgot.html'), name='password_reset'),

    path('forgot/passwd/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name = 'student/forgot_confirm.html'), name='password_reset_confirm'),

    path('forgot_passwd/send/', auth_views.PasswordResetDoneView.as_view(
        template_name = 'student/forgot_reset.html'), name='password_reset_done'),

    path('forgot_passwd/complete', auth_views.PasswordResetCompleteView.as_view(
        template_name = 'student/forgot_complete.html'), name= 'password_reset_complete'),

]
