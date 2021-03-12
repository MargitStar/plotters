from django.contrib import admin
from .models import Cutout, CutoutAdmin

admin.site.register(Cutout, CutoutAdmin)
