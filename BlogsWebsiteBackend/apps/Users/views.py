from rest_framework import viewsets, permissions
from .models import User
from .serializers import ProfileSerializer


class ProfileViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ('get', 'retrieve')

    def get_queryset(self):
        email = self.request.user.email
        return User.objects.filter(email=email)
