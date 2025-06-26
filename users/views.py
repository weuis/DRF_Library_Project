from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from users.serializers import UserRegisterSerializer, UserDetailSerializer

User = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
