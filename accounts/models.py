from django.db import models
from django.contrib.auth.models import AbstractUser

class EmployeeUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)