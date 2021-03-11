from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterApi, UserApi, UserDetailView

app_name = 'authentication'
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterApi.as_view(), name='register'),
    path('crud/', UserApi.as_view(), name='users'),
    path('user/<int:pk>/', UserDetailView.as_view(), name="user")
]
