from django.contrib import admin
from django.urls import path, include
from .views import PlotterView

app_name = 'plotters'
urlpatterns = [
    path('', PlotterView.as_view()),
]
