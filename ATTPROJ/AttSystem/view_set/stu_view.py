from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render
from AttSystem.models import *
from django.core.mail import send_mail
@login_required
@permission_required('AttSystem.add_student', raise_exception=True)
def add_student(request):
    if request.method == 'GET':
        return render(request,'add_student.html')
    elif request.method == 'POST':
        student_id = int(request.POST.get("student_id"))
        DOB = request.POST.get("DOB")
        attend = request.POST.get("attend")
        username = request.POST.get("username")
        course1 = request.POST.get("course1")
        print(course1)
        c = course1.split(',') #按照逗号分割字符串
        print(c)
        #当前c是一个包含所有要添加课程的列表，通过遍历c中的课程，可以获取到各个课程的名字，
        # 通过名字查询课程对象，然后加入到student里面
        #c[0] = 'WEB1'
        Course.objects.get(name=c[0])
        # try:
        #     myuser = User.objects.get(username=username)
        #     stu = Student.objects.create(student_id=student_id,DOB=DOB,attend=attend,user=myuser)
        # except Exception as e:
        #     print(e)
        return HttpResponse("ok")


@login_required
@permission_required('AttSystem.view_student', raise_exception=True)
def select_student(request):
    if request.method == 'GET':
        #把所有的学生查询出来，并返回
        stu = Student.objects.all()
        return render(request, 'select_student.html', {"stu":stu})

@login_required
@permission_required('AttSystem.change_student', raise_exception=True)
def change_student(request):
    if request.method == 'GET':
        sid = request.GET.get("id")
        stu = Student.objects.get(student_id=sid)
        users = User.objects.all() #查询出所有的用户
        myuser = stu.user
        courses = Course.objects.all()
        mycourse = stu.mycourse.all() #多对多关系要用all()
        check_id = [] #关联的课程id
        for i in mycourse:
            check_id.append(i.id)
        return render(request, 'change_student.html', {"stu":stu, "users":users, "myuser":myuser, "courses":courses, "check_id":check_id})
    elif request.method == 'POST':
        sid = request.POST.get("student_id")
        attend = request.POST.get("attend")
        DOB = request.POST.get("DOB")
        usertags = request.POST.getlist("tags")
        coursetags = request.POST.getlist("coursetags") #[所有选中课程的id]
        try:
            stu = Student.objects.get(student_id=sid)
            stu.DOB = DOB
            stu.attend = attend
            if len(usertags) > 1:
                return HttpResponse("只能选择一位用户！")
            myuser = User.objects.get(username=usertags[0])
            stu.user = myuser
            stu.mycourse.set(coursetags) #coursetags是id列表 或者传对象列表
            stu.save()
            return HttpResponse("ok")
        except Exception as e:
            print(e)
            return HttpResponse("error!")


@login_required
@permission_required('auth.view_user', raise_exception=True)
def send_email(request):
    if request.method == 'GET':
        sid = request.GET.get("id")
        stu = Student.objects.get(student_id=sid)
        return render(request, 'send.html', {"stu":stu})
    elif request.method == 'POST':
        subject = request.POST.get("subject")
        content = request.POST.get("content")
        to = request.POST.get("to")
        try:
            send_mail(subject=subject, message=content, recipient_list=[to,], from_email="752785200@qq.com")
            return HttpResponse("ok")
        except Exception as e:
            print(e)
            return HttpResponse("error")



@login_required
@permission_required('AttSystem.view_student', raise_exception=True)
def stu_class(request):
    if request.method == 'GET':
        #把所有的学生查询出来，并返回
        stu = Student.objects.all()
        return render(request, 'stu_class.html', {"stu":stu})


@login_required
@permission_required('AttSystem.change_student', raise_exception=True)
def enroll(request):
    if request.method == 'GET':
        sid = request.GET.get("id")
        stu = Student.objects.get(student_id=sid)
        myclass = stu.myclass.all()
        classes = Class.objects.all()
        check_id = [] #关联的课程id
        for i in myclass:
            check_id.append(i.id)
        return render(request, 'enroll.html', {"stu":stu, "classes":classes, "check_id":check_id})
    elif request.method == 'POST':
        sid = request.POST.get("stu_id")
        classtags = request.POST.getlist("ctags") #[所有选中课程的id]
        try:
            stu = Student.objects.get(student_id=sid)
            stu.myclass.set(classtags) #coursetags是id列表 或者传对象列表
            stu.save()
            return HttpResponse("ok")
        except Exception as e:
            print(e)
            return HttpResponse("error!")
