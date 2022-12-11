from rest_framework import serializers
from .models import User
from Blogs.models import Post
from Blogs.serializers import PostSerializer
import logging

logger = logging.getLogger('main')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.SerializerMethodField()

    def get_posts(self, request):
        logger.info('Showing only approved posts on the user\'s profile!')
        qs = Post.objects.filter(status='APPROVED')
        serializer = PostSerializer(instance=qs, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = User
        fields = ('id', 'email', 'user_name', 'first_name', 'last_name', 'posts')
