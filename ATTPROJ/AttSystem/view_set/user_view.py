from datetime import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from AttSystem.models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
@login_required
@permission_required('auth.add_user', raise_exception=True)
def add_user(request):
    if request.method == 'GET':
        return render(request,'add_user.html')
    elif request.method == 'POST':
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        telephone = request.POST.get("telephone")
        group = request.POST.get("select_group")
        print(f'group:{group}')
        try:
            #User是django中的
            myuser = User.objects.create_user(username=username,email=email,password=pwd,first_name=first_name,last_name=last_name)
            # myuser.save()
            UserProfile.objects.create(user=myuser,address=address,telephone=telephone)
            # global gp
            if group == '0':
                gp = Group.objects.get(name='Admin')
            elif group == '1':
                gp = Group.objects.get(name='Lecturer')
            elif group == '2':
                gp = Group.objects.get(name='Student')
            print(f'gp:{gp}')
            myuser.groups.add(gp)
            myuser.save() #add()方法需要save()
            return HttpResponse("ok")
        except Exception as e:
            print(e)
            return HttpResponse("error")

@login_required
@permission_required('auth.view_user', raise_exception=True)
def select_user(request):
    if request.method == 'GET':
        users = UserProfile.objects.all()#取了所有的userprofile
        for i in users:
            print(i.user.groups.all())

        return render(request,'select_user.html',{"users":users})

@login_required
@permission_required('auth.change_user', raise_exception=True)
def change_user(request):
    if request.method == 'GET':
        username = request.GET.get("username")
        myuser = User.objects.get(username=username)
        up = UserProfile.objects.get(user=myuser) #获取对应的userprofile
        return render(request, 'change_user.html', {"myuser":myuser, "up":up})
    elif request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        address = request.POST.get("address")
        telephone = request.POST.get("telephone")
        group = request.POST.get("select_group")
        try:
            myuser = User.objects.get(username=username)
            myuser.email = email
            myuser.first_name = first_name
            myuser.last_name = last_name
            if group == '0':
                gp = Group.objects.get(name='Admin')
            elif group == '1':
                gp = Group.objects.get(name='Lecturer')
            elif group == '2':
                gp = Group.objects.get(name='Student')
            #get取出来是一个对象（object) filter是queryset
            #query list

            #用一个列表 存很多个id
            #用一个列表，里面有很多个对象
            #[gp]
            myuser.groups.set([gp]) #set方法需要传一个列表
            myuser.save()
            up = UserProfile.objects.get(user=myuser)
            up.address = address
            up.telephone = telephone
            up.save()
            return HttpResponse("ok")
        except Exception as e:
            print(e)
            return HttpResponse("error")

def delete_user(request):
    uname = request.GET.get("username")
    print(f'iuuuu:{uname}')
    u = User.objects.get(username=uname)
    u.delete()
    return HttpResponse("ok")