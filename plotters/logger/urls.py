from django.urls import path
from .views import CutoutView

app_name = 'logger'
urlpatterns = [
    path('', CutoutView.as_view()),
]
