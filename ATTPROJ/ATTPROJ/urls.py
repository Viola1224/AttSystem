"""ATTPROJ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
import django.contrib.auth.views
from django.contrib import admin
from django.urls import path

import AttSystem.view_set.stu_view
from AttSystem import views
from AttSystem.view_set import stu_view, login_view, class_view, user_view, course_view, semester_view, lecturer_view
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view.login_v, name='login'),
    path('logout/', login_view.logout_v, name='logout'),
    path('', views.index, name='index'),
    path('welcome/',login_view.welcome, name='welcome'),
    path('add_user/', user_view.add_user, name='add_user'),
    path('select_user/', user_view.select_user, name='select_user'),
    path('change_user/', user_view.change_user, name='change_user'),
    path('delete_user/', user_view.delete_user, name='delete_user'),
    path('add_course/', views.add_course, name='add_course'),
    path('select_course/', course_view.select_course, name='select_course'),
    path('change_course/', course_view.change_course, name='change_course'),
    path('delete_course/', course_view.delete_course, name='delete_course'),

    path('add_lecturer/', views.add_lecturer, name='add_lecturer'),
    path('select_lecturer/', lecturer_view.select_lecturer, name='select_lecturer'),
    path('change_lecturer/', lecturer_view.change_lecturer, name='change_lecturer'),
    path('lecturer_class', lecturer_view.lecturer_class, name='lecturer_class'),
    path('assign', lecturer_view.assign, name='assign'),
    path('upload_file/', lecturer_view.upload_file, name='upload_file'),

    path('add_semester/', views.add_semester, name='add_semester'),
    path('select_semester', semester_view.select_semester, name='select_semester'),
    path('change_semester', semester_view.change_semester, name='change_semester'),

    path('add_student/', stu_view.add_student, name='add_student'),
    path('select_student/', stu_view.select_student, name='select_student'),
    path('change_student/', stu_view.change_student, name='change_student'),
    path('stu_class/', stu_view.stu_class, name='stu_class'),
    path('enroll/', stu_view.enroll, name='enroll'),


    path('add_class/', class_view.add_class, name='add_class'),
    path('select_class/', class_view.select_class, name='select_class'),
    path('change_class/', class_view.change_class, name='change_class'),

    path('send_email/', stu_view.send_email, name='send_email'),
]
