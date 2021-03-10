from django.contrib import admin
from django.urls import path, include
from .views import PlotterView, PlotterDetailView

app_name = 'plotters'
urlpatterns = [
    path('', PlotterView.as_view()),
    path('<int:pk>/', PlotterDetailView.as_view())
]
