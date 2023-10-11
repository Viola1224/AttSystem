from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from AttSystem.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission

def login_v(request):
    next = request.GET.get("next")
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        # print(request.body.decode())
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        user = authenticate(username=username,password=pwd) #根据用户名和密码验证用户
        print(next)
        print(username,  pwd)
        if user : #找到一个对应的用户
            print(f'user.is_active:{user.is_active}')
            if user.is_active==True: #如果用户是active的
                login(request,user)
                # print(Permission.objects.all())
                return HttpResponse("ok")
        else:
            return HttpResponse("error")

def logout_v(request):
    logout(request) #退出登录 清除用户数据
    return redirect('login')

def welcome(request):
    return render(request, 'welcome.html')