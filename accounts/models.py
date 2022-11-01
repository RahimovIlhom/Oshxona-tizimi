from django.db import models
from django.contrib.auth.models import AbstractUser

class EmployeeUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)