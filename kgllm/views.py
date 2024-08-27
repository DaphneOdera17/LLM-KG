from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from kgllm.models import UserInfo
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password

def index(request):
    if 'user_id' in request.session:
        try:
            user = UserInfo.objects.get(id=request.session['user_id'])
        except UserInfo.DoesNotExist:
            user = None
        return render(request, "index.html", {"user": user})
    else:
        return redirect("/login/")


def logout_view(request):
    request.session.flush()
    return redirect('/login/')


def user_list(request):
    return render(request, "user_list.html")

def user_add(request):
    return HttpResponse("添加用户")

# def login_view(request):
#     if request.method == "GET":
#         return render(request, "login.html")
#     else:
#         username = request.POST.get("user")
#         password = request.POST.get("pwd")
#
#         try:
#             obj = UserInfo.objects.get(name=username)
#         except UserInfo.DoesNotExist:
#             obj = None
#
#         if obj is not None and obj.password == password:
#             request.session['user_id'] = obj.id
#             return render(request, "login.html", {"message": "登录成功!"})
#         else:
#             return render(request, "login.html", {"error_msg": "用户名或密码错误"})

def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST.get("user")
        password = request.POST.get("pwd")

        try:
            user = UserInfo.objects.get(name=username)
        except UserInfo.DoesNotExist:
            user = None

        if user and check_password(password, user.password):
            request.session['user_id'] = user.id
            return JsonResponse({'redirect': '/index/', 'message': '登录成功!'})
        else:
            return JsonResponse({'error': '用户名或密码错误'})

def register(request):
    if request.method == "GET":
        return render(request, "register.html")

    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    email = request.POST.get("email")

    if not user or not pwd or not email:
        return JsonResponse({'error': '所有字段都是必填的！'})

    if UserInfo.objects.filter(name=user).exists():
        return JsonResponse({'error': '用户名已存在！'})

    encrypted_password = make_password(pwd)

    UserInfo.objects.create(name=user, password=encrypted_password, email=email)
    return JsonResponse({'redirect': '/login/', 'message': '注册成功！'})

def home(request):
    return render(request, 'index.html')

def kgqa(request):
    return render(request, "kgqa.html")


