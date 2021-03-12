from django.db import models
from django.contrib.auth import get_user_model
from plotter.models import Plotter
from mold.models import Mold
import datetime

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

    created_date = models.DateTimeField(
        default=datetime.datetime.now()
    )
