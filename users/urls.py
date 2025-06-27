from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import UserRegisterView, UserMeView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", UserMeView.as_view(), name="user-me"),
]
