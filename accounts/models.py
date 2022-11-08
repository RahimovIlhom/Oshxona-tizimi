from django.db import models
from django.contrib.auth.models import AbstractUser

class EmployeeUser(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    STATUS = (
        ('cashier', ('kassir')),
        ('cook', ('oshpaz')),
        ('accountant', ('buxgalter')),
    )

    # […]
    profession = models.CharField(
        max_length=32,
        choices=STATUS,
        default='cashier',
    )