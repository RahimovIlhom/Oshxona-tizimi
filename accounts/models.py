from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse


class EmployeeUser(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    STATUS = (
        ('cashier', ('kassir')),
        ('chef', ('oshpaz')),
        ('accountant', ('buxgalter')),
    )

    # […]
    profession = models.CharField(
        max_length=32,
        choices=STATUS,
        default='cashier',
    )

    def get_delete_user_view_url(self):
        return reverse('delete_user', kwargs={
            'username': self.username
        })