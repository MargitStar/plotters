from django.urls import path
from .views import CutoutView, CutoutDetailView, MoldView

app_name = 'logger'
urlpatterns = [
    path('', CutoutView.as_view()),
    path('<int:pk>/', CutoutDetailView.as_view()),
    path('mold/', MoldView.as_view()),
]
