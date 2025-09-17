from django.db import models

class User(models.Model):
    name = models.CharField(max_length=64)
    tag = models.CharField(max_length=32)
    groups = models.ManyToManyField("Group")

    def __str__(self):
        return f"@{self.tag}"

class Group(models.Model):
    name = models.CharField(max_length=64)
    members = models.ManyToManyField("User")

    def add_member(self,user : User):
        user.groups.add(self)
        self.members.add(user)

    def __str__(self):
        return f"{self.name}"