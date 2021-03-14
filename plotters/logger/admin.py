from django.contrib import admin
from .models import Cutout, CutoutAdmin, MoldStatistics, MoldStatisticsAdmin, PlotterStatistics, PlotterStatisticsAdmin

admin.site.register(Cutout, CutoutAdmin)
admin.site.register(MoldStatistics, MoldStatisticsAdmin)
admin.site.register(PlotterStatistics, PlotterStatisticsAdmin)
