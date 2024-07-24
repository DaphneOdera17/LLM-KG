from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path

from kgllm import views

urlpatterns = [
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('index/', views.index, name='index'),
    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('login/', views.login),
    path('register/', views.register),
    path('kgqa/', views.kgqa, name='kgqa'),
    path('contact/', views.contact, name='contact'),
]
