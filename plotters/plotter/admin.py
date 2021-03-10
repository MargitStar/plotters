from django.contrib import admin
from .models import Plotter, PlotterAdmin


admin.site.register(Plotter, PlotterAdmin)
