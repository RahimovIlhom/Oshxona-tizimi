from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

class Profession(models.Model):
    name = models.CharField(max_length=20)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('profession', args=[str(self.name)])

