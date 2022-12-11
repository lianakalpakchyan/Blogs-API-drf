from rest_framework import viewsets, permissions
from .models import User
from .serializers import ProfileSerializer
import logging

logger = logging.getLogger('main')


class ProfileViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ('get', 'retrieve')

    def get_queryset(self):
        logger.info('Showing the current user\'s profile!')
        email = self.request.user.email
        return User.objects.filter(email=email)
