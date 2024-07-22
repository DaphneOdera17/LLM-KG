from django.http import HttpResponse
from django.shortcuts import render, redirect

from kgllm.models import UserInfo


def index(request):
    return render(request, "index.html")

def user_list(request):
    return render(request, "user_list.html")

def user_add(request):
    return HttpResponse("添加用户")

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        # print(request.POST)
        username = request.POST.get("user")
        password = request.POST.get("pwd")

        try:
            obj = UserInfo.objects.filter(name=username).first()
        except UserInfo.DoesNotExist:
            obj = None

        if obj is not None and obj.password == password:
            request.session['user_id'] = obj.id
            return redirect("/index/")
        else:
            return render(request, "login.html")

def register(request):
    if request.method == "GET":
        return render(request, "register.html")

    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    email = request.POST.get("email")

    if not user or not pwd or not email:
        return render(request, "register.html", {"error_msg": "所有字段都是必填的！"})
    else:
        UserInfo.objects.create(name=user, password=pwd, email=email)
        return redirect("/index/")
