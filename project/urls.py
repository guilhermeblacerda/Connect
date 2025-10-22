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

from student import views as studentViews
from teacher import views as teacherViews

urlpatterns = [
    path('', studentViews.login_page, name="login"),

    path('register/',studentViews.register_page, name="register"),

    path('home/', studentViews.home_page, name="home"),

    path('admin/', admin.site.urls, name="admin"),

    path('absence/', studentViews.absence_page, name="absence"),

    path('score/', studentViews.score_page, name="score"),

    path('calendar/', studentViews.calendar_page, name="calendar"),

    path('logout/', studentViews.logout_page, name="logout"),

    path('teacher/login/', teacherViews.GoToLogin, name ="teacherLogin"),

    path('teacher/', teacherViews.GoToHome, name = "teacherHome"),

    path('teacher/absence/',teacherViews.GoToAbsence, name ="teacherAbsence"),

    path('teacher/absence/<int:serieId>/<int:materiaId>/',teacherViews.GoToAbsence, name ="teacherAbsenceDetail"),

    path('teacher/score/', teacherViews.GoToScore, name = "teacherScore"),

    path('teacher/score/<int:serieId>/<int:materiaId>/',teacherViews.GoToScore,name = "teacherScoreDetail"),

    path('teacher/score/<int:serieId>/<int:materiaId>/<int:alunoId>/',teacherViews.GoToScore,name = "teacherScoreAluno"),

    path('chat/', studentViews.chat_page , name = "chat"),

    path('chat/<int:usuario_id>/', studentViews.chat_page, name='chat'), 

    path('forgot_passwd/',auth_views.PasswordResetView.as_view(
        template_name = 'student/forgot.html'), name='password_reset'),

    path('forgot/passwd/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name = 'student/forgot_confirm.html'), name='password_reset_confirm'),

    path('forgot_passwd/send/', auth_views.PasswordResetDoneView.as_view(
        template_name = 'student/forgot_reset.html'), name='password_reset_done'),

    path('forgot_passwd/complete', auth_views.PasswordResetCompleteView.as_view(
        template_name = 'student/forgot_complete.html'), name= 'password_reset_complete'),

]
