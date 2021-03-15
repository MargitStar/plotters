from django.urls import path
from .views import CutoutView, CutoutDetailView, MoldView, PlotterView

app_name = 'logger'
urlpatterns = [
    path('', CutoutView.as_view()),
    path('<int:pk>/', CutoutDetailView.as_view()),
    path('mold/', MoldView.as_view()),
    path('plotter/', PlotterView.as_view())
]
