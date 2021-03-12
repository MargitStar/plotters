from django.contrib import admin
from .models import Cutout, CutoutAdmin, MoldStatistics

admin.site.register(Cutout, CutoutAdmin)
admin.site.register(MoldStatistics)