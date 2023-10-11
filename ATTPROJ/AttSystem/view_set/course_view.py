from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from AttSystem.models import *
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

@login_required
@permission_required('AttSystem.view_course', raise_exception=True)
def select_course(request):
    if request.method == 'GET':
        mycourse = Course.objects.all() #查询出所有课程对象
        return render(request,'select_course.html',{"mycourse":mycourse})

@login_required
@permission_required('AttSystem.change_course',raise_exception=True)
def change_course(request):
    if request.method == 'GET':
        #接收传来的id
        id = request.GET.get("id")
        c = Course.objects.get(id=id)
        return render(request, 'change_course.html', {"c":c})
    elif request.method == 'POST':
        course_id = request.POST.get("course_id")
        course_code = request.POST.get("course_code")
        course_name = request.POST.get("course_name")
        try:
            c = Course.objects.get(id=course_id)
            c.name = course_name
            c.code = course_code
            c.save()
            return HttpResponse("ok")
        except Exception as e:
            print(e)
            return HttpResponse("error")

@login_required
@permission_required('AttSystem.delete_course', raise_exception=True)
def delete_course(request):
    id = request.GET.get("id")
    try:
        c = Course.objects.get(id=id)
        c.delete()
        return redirect('select_course')
    except Exception as e:
        print(e)
        return HttpResponse("error")