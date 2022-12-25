from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer
)
import logging

logger = logging.getLogger('main')


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        save_reply = serializer.save()
        if save_reply is None:
            response_message = {"message": "User successfully logged out!"}
            return Response(response_message, status=status.HTTP_204_NO_CONTENT)
        else:
            logger.error(save_reply)
            response_message = {"message": str(save_reply)}
            return Response(response_message, status=status.HTTP_400_BAD_REQUEST)
