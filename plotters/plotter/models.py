from django.db import models
from django.contrib import admin
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

    def users(self):
        return ",".join([str(user) for user in self.user.all()])

    def __str__(self):
        return f"Plotter # {self.serial_number}"


class PlotterAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'users']
    list_display_links = ['serial_number']
