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

    ip = models.GenericIPAddressField(
        default='127.0.0.1'
    )

    cutouts = models.IntegerField(
        "Allowed cutouts",
        default=0
    )

    def users(self):
        return ",".join([str(user) for user in self.user.all()])

    def __str__(self):
        return f"Plotter # {self.serial_number}"


class PlotterAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'users', 'ip', 'cutouts']
    list_display_links = ['serial_number']
