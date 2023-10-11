from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from AttSystem.models import *
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

@login_required
@permission_required('AttSystem.view_semester', raise_exception=True)
def select_semester(request):
    if request.method == 'GET':
        clist = [] #存储各个学期的课程
        mysemester = Semester.objects.all()
        return render(request, 'select_semester.html', {"mysemester":mysemester})

@login_required
@permission_required('AttSystem.change_semester',raise_exception=True)
def change_semester(request):
    if request.method == 'GET':
        #接收传来的id
        id = request.GET.get("id") #url中的传的id参数
        s = Semester.objects.get(id=id) #当前查询的学期
        c = s.course.all() #这个学期关联的所有课程
        courses = Course.objects.all() #查询出数据库中所有的课程
        #什么可以唯一的确定一个课程？-》用id
        #用一个列表 把我们需要选中的课程id都存一块
        # print(f'这个学期的所有课程:{c}')
        # print(f'数据库中所有课程：{courses}')
        check_id = []
        for x in c:
            check_id.append(x.id)
        #现在，check_id里面存了跟当前学期关联的课程id
        # print(check_id)
        return render(request, 'change_semester.html', {"s":s, "courses":courses, "check_id":check_id})
    elif request.method == 'POST':
        tags = request.POST.getlist("tags")
        semester_id = request.POST.get("semester_id")
        year = request.POST.get("year")
        semester = request.POST.get("semester")
        # clist = [] #用一个列表 存储change后的 当前学期的课程
        # for cid in tags:
        #     #查询checked课程
        #     c = Course.objects.get(id=cid)
        #     clist.append(c)
        # print(clist)
        try:
            s = Semester.objects.get(id=semester_id) #根据id查出对应的学期
            s.year = year
            s.semester = semester
            s.course.set(tags) #tags里面存的是课程id
            s.save()
            return HttpResponse("ok")
        except Exception as e:
            print(e)
            return HttpResponse("error")