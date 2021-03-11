from django.urls import path
from .views import MoldView

app_name = 'mold'
urlpatterns = [
    path('', MoldView.as_view())
]
