from django.urls import path
from .views import CutoutView, CutoutDetailView

app_name = 'logger'
urlpatterns = [
    path('', CutoutView.as_view()),
    path('<int:pk>/', CutoutDetailView.as_view())
]
