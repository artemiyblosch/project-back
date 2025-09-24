from django.db import models
import re
from typing import Self
from django.contrib.auth.models import AbstractBaseUser as U

class User(U):
    tag = models.CharField(max_length=32)
    name = models.CharField(max_length=1024)

    def __str__(self):
        return f"@{self.tag}"
    
    def text(self, group, text : str):
        m = Message(text=text, owner=self, group=group)
        m.save()
        for i in re.finditer(r'@\S+',text):
            m.referants.add(User.objects.filter(tag=i.group()[1:])[0])
        return m

    def json(self):
        return {"name": self.name, "password": self.password, "tag": self.tag}

    @staticmethod
    def find_by_tag(tag : str) -> Self:
        return User.objects.filter(tag=tag)[0]

class Group(models.Model):
    name = models.CharField(max_length=64)
    members = models.ManyToManyField("User",related_name="member_in")

    def add_member(self,user : User):
        user.groups.add(self)
        self.members.add(user)

    def __str__(self):
        return f"{self.name}"
    
class Message(models.Model):
    text = models.CharField(max_length=65536)
    owner = models.ForeignKey("User",related_name="messages",on_delete=models.SET_NULL,null=True)
    referants = models.ManyToManyField("User", related_name="refered_in")
    group = models.ForeignKey("Group", on_delete = models.CASCADE, related_name="messages")

    def __str__(self):
        return f"{self.owner} in {self.group.name}: {self.text}"