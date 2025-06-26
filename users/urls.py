from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import UserRegisterView, UserMeView

urlpatterns = [
    path("users/", UserRegisterView.as_view(), name="user-register"),
    path("users/token/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("users/me/", UserMeView.as_view(), name="user-me"),
]
