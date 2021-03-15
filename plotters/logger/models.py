from datetime import date
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib import admin

from plotter.models import Plotter
from mold.models import Mold

User = get_user_model()


class Cutout(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='user'
    )

    plotter = models.ForeignKey(
        Plotter,
        on_delete=models.PROTECT,
        related_name='plotter'
    )

    mold = models.ForeignKey(
        Mold,
        on_delete=models.PROTECT,
        related_name='mold'
    )

    amount = models.IntegerField(
        default=0,
    )

    created_date = models.DateTimeField(
        'Time',
    )


class CutoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'plotter', 'mold', 'created_date', 'amount']


class MoldStatistics(models.Model):
    plotter = models.ForeignKey(
        Plotter,
        on_delete=models.PROTECT,
    )

    mold = models.ForeignKey(
        Mold,
        on_delete=models.PROTECT,
    )

    cutouts = models.IntegerField(
    )


class MoldStatisticsAdmin(admin.ModelAdmin):
    list_display = ['plotter', 'mold', 'cutouts']


class PlotterStatistics(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1
    )

    plotter = models.ForeignKey(
        Plotter,
        on_delete=models.PROTECT,
    )

    ip = models.GenericIPAddressField(

    )

    cutouts = models.IntegerField()

    last_cutout_date = models.DateField(
        default=date.today
    )


class PlotterStatisticsAdmin(admin.ModelAdmin):
    list_display = ['plotter', 'ip', 'cutouts']
