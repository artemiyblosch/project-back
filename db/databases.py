from django.db import models
from django.core.validators import int_list_validator

class Group(models.Model):
    name = models.CharField(max_length=64)
    participants = models.CharField(validators=[int_list_validator], max_length=100)