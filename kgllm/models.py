from django.db import models

# MySQL 表
class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    email = models.EmailField(default="")
