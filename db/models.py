from django.db import models
#import re
from typing import Self
from django.contrib.auth.models import AbstractBaseUser as U
from django.http import HttpRequest
import json

def default_d():
    return {"ct": 0, "cool": 0, "sad": 0}

class User(U):
    tag = models.CharField(max_length=32)
    name = models.CharField(max_length=1024)
    USERNAME_FIELD = "name"

    def __str__(self):
        return f"@{self.tag}"
    
    @staticmethod
    def strict_find(req : HttpRequest, keys : list[str]):
        req_in_json : dict = json.loads(req.body)

        try:
            filter_query = {i: req_in_json[i] for i in keys}
            return User.objects.filter(**filter_query)
        except KeyError:
            return None
    
    def text(self, group, text : str, type : int):
        m = Message(text=text, owner=self, group=group, type=type)
        m.save()
        #for i in re.finditer(r'@\S+',text):
            #m.referants.add(User.objects.filter(tag=i.group()[1:])[0])
        return m

    def json(self):
        return self.safe_json() | {"password": self.password, "pk": self.pk}
    
    def safe_json(self):
        return {"name" : self.name, "tag": self.tag}

    @staticmethod
    def find_by_tag(tag : str) -> Self:
        return User.objects.filter(tag=tag)[0]

class Group(models.Model):
    name = models.CharField(max_length=64)
    members = models.ManyToManyField("User",related_name="member_in")
    vibes = models.JSONField(default=default_d)
    main_vibe = models.CharField(max_length=64, default="")

    def add_member(self,user : User):
        user.groups.add(self)
        self.members.add(user)
    
    def update_vibe(self):
        m = max(self.vibes, key=self.vibes.get)
        if self.main_vibe == "":
            self.main_vibe = m
        elif self.vibes[self.main_vibe] + 20 <= self.vibes[m]:
            self.main_vibe = m
        return self

    def json(self):
        return {"pk": self.pk, "name": self.name,\
                "members": [i.tag for i in self.members.all()], 
                "vibes" : self.vibes, 
                "main_vibe" : self.main_vibe}
    
    def short_json(self):
        return {"pk" : self.pk}

    @staticmethod
    def strict_find(req : HttpRequest, keys : list[str]):
        req_in_json : dict = json.loads(req.body)

        try:
            filter_query = {i: req_in_json[i] for i in keys}
            return Group.objects.filter(**filter_query)
        except KeyError:
            return None

    def __str__(self):
        return f"{self.name}"
    
class Message(models.Model):
    text = models.CharField(max_length=65536)
    owner = models.ForeignKey("User",related_name="messages",on_delete=models.SET_NULL,null=True)
    #referants = models.ManyToManyField("User", related_name="refered_in")
    group = models.ForeignKey("Group", on_delete = models.CASCADE, related_name="messages")
    type = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.owner} in {self.group.name}: {self.text}"
    
    def json(self):
        return {"text" : self.text, "owner" : self.owner.safe_json(), "group" : self.group.short_json(), "type" : self.type}