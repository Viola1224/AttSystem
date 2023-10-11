from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render
from AttSystem.models import *

@login_required
@permission_required('AttSystem.add_class', raise_exception=True)
def add_class(request):
    if request.method == 'GET':
        return render(request,'add_Class.html')
    elif request.method == 'POST':
        number = int(request.POST.get("number"))
        course = request.POST.get("course")
        lecturer = request.POST.get("lecturer")
        student = request.POST.get("student")
        semester = request.POST.get("semester")
        stu = student.split(',') #按照逗号分割字符串
        # for i in range(len(stu)):
        #     stu[i] = int(stu[i])
        # print(stu)
#['1','2','3']
        # for i in stu:

        try:
            mycourse = Course.objects.get(name=course) #获取课程对象
            mysemester = Semester.objects.get(semester=semester)
            mylecturer = Lecturer.objects.get(staff_id=lecturer)
            s = Student.objects.filter(student_id__in=stu)
            print(s)
            myclass = Class.objects.create(number=number,course=mycourse,Lecturer=mylecturer,semester=mysemester)
            myclass.student.add(*s)
        except Exception as e:
            print(e)
            return HttpResponse("Error!")
        return HttpResponse("ok")

@login_required
@permission_required('AttSystem.view_class', raise_exception=True)
def select_class(request):
    if request.method == 'GET':
        myclass = Class.objects.all()
        return render(request, 'select_class.html', {"myclass":myclass})

@login_required
@permission_required('AttSystem.change_class', raise_exception=True)
def change_class(request):
    if request.method == 'GET':
        id = request.GET.get("id")
        cla = Class.objects.get(id=id)
        #查询出所有的lecturer、course、semester
        lecturers = Lecturer.objects.all()
        courses = Course.objects.all()
        semesters = Semester.objects.all()
        mylecturer = cla.Lecturer
        mycourse = cla.course
        mysemester = cla.semester
        locals().update()
        return render(request, 'change_class.html',locals())
    elif request.method == 'POST':
        cid = request.POST.get("class_id")
        coursetags = request.POST.getlist("ctags") #课程
        if (len(coursetags))>1:
            return HttpResponse("error!")
        c = Course.objects.get(id=coursetags[0])
        cla = Class.objects.get(id=cid)
        cla.course = c
        cla.save()