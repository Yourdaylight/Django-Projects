from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import StudentModel, StudentInformationModel, CourseModel
from django.forms.models  import model_to_dict
# Create your views here.
import json
# 主界面
def index(request):
    context = {
        'status': '未登录状态'
    }
    return render(request, 'studentManage/index.html', context)

# 登录界面
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not all([username, password]):
            return HttpResponse('错误！用户名或密码为空！')
        else:
            student = StudentModel.objects.filter(username=username, password=password)
            if len(student):
                # 将用户的信息存放到session中，session在中间件中是默认启用的
                request.session['user'] = {
                    'id':student[0].stu_id,
                    'username': username,
                    'password': password
                }
                context = {
                    'status': username,
                    'msg': '已登录',
                    'lenght': 1
                }
                return render(request, 'studentManage/index.html',context)

            else:
                context = {
                    'msg': '用户名密码错误'
                }
                return render(request, 'studentManage/login.html', context)
    else:
        context = {
            'status': '未登录状态',
            'length': 0
        }
        return render(request, 'studentManage/login.html', context)
#注册界面
def regist(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        verif_password=request.POST.get("verif_password")
        student = StudentModel.objects.filter(username=username)
        #注册验证错误信息汇总
        error_message=""
        if not all([username,password,verif_password]):
            error_message+="注册信息不能为空;\n"
        if student:
            error_message+="该用户名已存在;\n"
        if password!=verif_password:
            error_message+="两次密码输入不一致;\n"
        #如果存在注册信息则重定向到注册页面
        if error_message:
            context = {
                "error": error_message
            }
            return render(request,'studentManage/regist.html',context)

        #注册信息有效，注册成功
        stu_data = StudentModel()
        stu_data.username= username
        stu_data.password=password
        stu_data.save()
        context = {
            'sucess': '增加成功',
        }
        return render(request, 'studentManage/login.html', context)

    else:
        return render(request, 'studentManage/regist.html')
# 退出界面
def logout(request):
    # 注销掉用户，从删除session中保存的信息
    del request.session['user']
    return render(request, 'studentManage/index.html')

# 增加数据 增加只能root用户或者管理员才能操作
def add(request):
    if request.method == "POST":
        root_information = request.session['user']
        id = root_information['id']
        root_id = StudentModel.objects.get(pk=id).stu_id
        if id == root_id:
            stu_name = request.POST.get('stu_name')
            if not all([stu_name]):
                context = {
                    'msg': '名字有遗漏',
                }
                return render(request, 'studentManage/add.html', context)

            stu_data = StudentInformationModel()
            stu_data.stu_name = stu_name
            stu_data.stu_phone = request.POST.get('stu_phone')
            stu_data.str_addr = request.POST.get('str_addr')
            stu_data.stu_faculty =request.POST.get('stu_faculty')
            stu_data.stu_major = request.POST.get('stu_major')
            stu_data.save()
            context = {
                'sucess': '增加成功',
            }
            return render(request, 'studentManage/add.html', context)
        else:
            context = {
                'error': '只用root用户和管理员才能操作'
            }
            return render(request, 'studentManage/add.html', context)
    else:
        return render(request, 'studentManage/add.html')


# 查询
def select(request):
    if request.method == "POST":
        id = request.POST.get('stu_id')
        if id=='':
            id=request.session['user']['id']
        print()
        stu_data = StudentInformationModel.objects.get(pk=id)

        stu_course = CourseModel.objects.filter(cour_id=id)
        dct = {}
        for stu in stu_course:
            dct[stu.course] = stu.grade
        context = {
            'stu_id': id,
            'stu_name': stu_data.stu_name,
            'stu_phone':stu_data.stu_phone,
            'str_addr': stu_data.str_addr,
            'stu_faculty':  stu_data.stu_faculty,
            'stu_major':  stu_data.stu_major,
            'course_data': dct,
            'msg': True
        }
        return render(request, 'studentManage/select.html', context)
    else:
        root_information = request.session['user']
        id = root_information['id']
        context = {
            'msg': False,
            'id': id
        }
        return render(request, 'studentManage/select.html', context)

# 删除
def delete(request):
    if request.method == "POST":
        id = int(request.POST.get('id'))
        StudentInformationModel.objects.filter(stu_id=id).delete()
        context = {
            'msg': '成功删除'
        }
        return render(request, 'studentManage/delete.html', context)
    else:
        root_information = request.session['user']
        id = root_information['id']
        context = {
            'id': id
        }
        return render(request, 'studentManage/delete.html', context)


# 修改
def update(request):
    user_information = request.session['user']
    id = user_information['id']
    stu_data = StudentInformationModel.objects.get(stu_id=id)
    context = {
            'stu_id': stu_data.stu_id,
            'stu_name': stu_data.stu_name,
            'stu_phone':stu_data.stu_phone,
            'str_addr': stu_data.str_addr,
            'stu_faculty':  stu_data.stu_faculty,
            'stu_major':  stu_data.stu_major,
    }
    if request.method == "POST":
        context['stu_id'] = request.POST.get('stu_id')
        context['stu_name'] = request.POST.get('stu_name')
        context['stu_phone'] = request.POST.get('stu_phone')
        context['stu_addr'] = request.POST.get('stu_addr')
        context['stu_faculty'] = request.POST.get('stu_faculty')
        context['stu_major'] = request.POST.get('stu_major')
        return render(request, 'studentManage/update.html', context)
    else:
        return render(request, 'studentManage/update.html', context)
