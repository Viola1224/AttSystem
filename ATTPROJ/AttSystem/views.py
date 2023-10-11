from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

@login_required #decorator 装饰器 限制必须登录后再访问
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'formTree.html')

@login_required
@permission_required('AttSystem.add_course', raise_exception=True)
def add_course(request):
    if request.method == 'GET':
        return render(request,'add_course.html')
    elif request.method == 'POST':
        #获取到前端传来的数据
        course_code = request.POST.get("course_code")
        course_name = request.POST.get("course_name")
        Course.objects.create(code=course_code, name=course_name)
        return HttpResponse("ok")
# datetime.strptime(,'%Y-%m-%d').date()

@login_required
def select_course(request):
    return render(request,'tableBasic.html')

@login_required
@permission_required('AttSystem.add_lecturer', raise_exception=True)
def add_lecturer(request):
    if request.method == 'GET':
        return render(request, 'add_lecturer.html')
    elif request.method == 'POST':
        staff_id = request.POST.get("staff_id")
        DOB = datetime.strptime(request.POST.get("DOB"),'%Y-%m-%d').date()
        username = request.POST.get("username")
        try:
            myuser = User.objects.get(username=username) #存一下查出来的user
            Lecturer.objects.create(staff_id=staff_id, DOB=DOB,user=myuser)

        except Exception as e: #所有的异常集合到这
            print(e)
            return HttpResponse("请输入正确的用户名")
        return HttpResponse("ok")

@login_required
@permission_required('AttSystem.add_semester', raise_exception=True)
def add_semester(request):
    if request.method == 'GET':
        return render(request, 'add_semester.html')
    elif request.method == 'POST':
        try:
            year = int(request.POST.get("year"))
            semester = request.POST.get("semester")
            course1 = request.POST.get("course1")
            course2 = request.POST.get("course2") #两个课程名
            courses = Course.objects.filter(name__in=[course1, course2]) #筛选出两个课程
            S = Semester.objects.create(year=year, semester=semester) #创建一个学期对象，里面还没有添加多对多的内容
            S.course.add(*courses)
            S.save()
        except Exception as e:
            print(e)
            return HttpResponse("uncorrect!")
        return HttpResponse("ok")

