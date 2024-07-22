from django.contrib import admin
from django.urls import path

from kgllm import views

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('index/', views.index),
    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('login/', views.login),
    path('register/', views.register),
]
