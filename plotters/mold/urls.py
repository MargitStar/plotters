from django.urls import path
from .views import MoldView, MoldDetailView

app_name = 'mold'
urlpatterns = [
    path('', MoldView.as_view()),
    path('<int:pk>', MoldDetailView.as_view())
]
