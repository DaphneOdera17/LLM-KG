from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path

from kgllm import views

urlpatterns = [
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('index/', views.index, name='index'),
    path('user/add/', views.user_add),
    path('login/', views.login_view, name='login'),
    path('register/', views.register),
    path('kgqa/', views.chat_view, name='kgqa'),
    path('logout/', views.logout_view, name='logout'),
    path('kg/', views.kg_view, name='kg'),
]
