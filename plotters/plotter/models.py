from django.db import models
from django.contrib.auth.models import User


class Plotter(models.Model):
    serial_number = models.CharField(
        'Serial Number',
        max_length=150,
        unique=True
    )

    user = models.ManyToManyField(
        User,
    )

    def __str__(self):
        return f"Plotter # {self.serial_number}"
