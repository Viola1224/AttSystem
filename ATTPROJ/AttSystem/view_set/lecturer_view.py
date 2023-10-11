from datetime import datetime
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from AttSystem.models import *
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

@login_required
@permission_required('AttSystem.view_lecturer', raise_exception=True)
def select_lecturer(request):
    if request.method == 'GET':
        l = Lecturer.objects.all()
        return render(request, 'select_lecturer.html', {"mylecturer":l})

@login_required
@permission_required('AttSystem.change_lecturer', raise_exception=True)
def change_lecturer(request):
    if request.method == 'GET':
        staff_id = request.GET.get("id")
        l = Lecturer.objects.get(staff_id=staff_id)
        myuser = l.user #当前关联的user
        users = User.objects.all() #所有的user
        return render(request, 'change_lecturer.html', {"l":l, "myuser":myuser, "users":users})
    elif request.method == 'POST':
        tags = request.POST.getlist("tags") #["1"]
        print(f'tags:{tags}')
        staff_id = request.POST.get("lecturer_id")
        DOB = request.POST.get("DOB")
        try:
            l = Lecturer.objects.get(staff_id=staff_id)
            l.DOB = DOB
            #查询user
            myuser = User.objects.get(username=tags[0])
            l.user = myuser
            l.save()
            return HttpResponse("ok")
        except Exception as e:
            print(e)
            return HttpResponse("error")



@login_required
@permission_required('AttSystem.change_student', raise_exception=True)
def upload_file(request):
    if request.method == 'GET':
        return render(request, 'upload_file.html')
    elif request.method == "POST" and request.FILES['stu_file']:
        stufile = request.FILES['stu_file'] #获取前端上传的文件
        fs = FileSystemStorage()
        file = fs.save(stufile.name,stufile) #上传的文件保存在media中

        data = pd.read_excel(stufile)
        data = pd.DataFrame(data, columns=[
            "student_id", "attend"
        ]) #提取出student_id&attend这两列数据
        stu_id = data["student_id"].tolist() #把student_id这一列的数据 转为列表
        attend = data["attend"].tolist()
        #stu_id=[1,10]
        #attend=[0.5,0.9]
        for i in range(len(stu_id)):
            student = Student.objects.get(student_id=stu_id[i]) #查出来student
            student.attend = attend[i]
            student.save()
        return redirect('select_student')


@login_required
@permission_required('AttSystem.view_lecturer', raise_exception=True)
def lecturer_class(request):
    if request.method == 'GET':
        classes = Class.objects.all()
        return render(request, 'lec_class.html', {"classes":classes})

@login_required
@permission_required('AttSystem.change_class', raise_exception=True)
def assign(request):
    if request.method == 'GET':
        id = request.GET.get("id")
        cla = Class.objects.get(id=id)
        #查询出所有的lecturer、course、semester
        lecturers = Lecturer.objects.all()
        mylecturer = cla.Lecturer
        locals().update()
        return render(request, 'assign.html',locals())
    elif request.method == 'POST':
        cid = request.POST.get("class_id")
        ltags = request.POST.getlist("ltags") #lecturer
        if (len(ltags))>1:
            return HttpResponse("error!")
        try:
            l = Lecturer.objects.get(id=ltags[0])
            cla = Class.objects.get(id=cid)
            cla.Lecturer = l
            cla.save()
            return HttpResponse("ok")
        except Exception as e:
            print(e)
            return HttpResponse("error")