from django.db import models


class Plotter(models.Model):
    serial_number = models.CharField(
        name='Serial Number',
        max_length=150,
        unique=True
    )

    def __str__(self):
        return f"Plotter # {self.pk}"
