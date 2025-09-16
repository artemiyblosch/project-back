from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=64)
    members = models.ManyToManyField("User")

class User(models.Model):
    name = models.CharField(max_length=64)
    tag = models.CharField(max_length=32)
    groups = models.ManyToManyField(Group)