from django.db import models
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom

# MySQL 表
class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    email = models.EmailField(default="")

class Person(GraphObject):
    __primarykey__ = "name"

    name = Property()
    age = Property()

    friends = RelatedTo("Person")
    knows = RelatedTo("Person")
    family = RelatedTo("Person")
