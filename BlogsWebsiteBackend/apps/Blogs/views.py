from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
import logging

logger = logging.getLogger('main')


class PostViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('hash_tag', 'category', 'author', 'status')
    search_fields = ('title', 'hash_tag__name')
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ('get', 'post', 'retrieve', 'put', 'delete')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if instance.status != 'NULL' and (request.user == instance.author or request.user.is_staff) \
                or instance.status == 'NULL' and request.user.is_staff:
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            response_message = {"message": "Not Allowed! Post is pending or you are not authorized"}
            logger.debug("The post can't be updated by the user as it's pending or user is not authorized!")
            return Response(response_message, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'NULL' and (request.user == instance.author or request.user.is_staff) \
                or instance.status == 'NULL' and request.user.is_staff:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            response_message = {"message": "Not Allowed! Post is pending or you are not authorized!"}
            logger.debug("The post can't be deleted by the user as it's pending or user is not authorized!")
            return Response(response_message, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'retrieve']
