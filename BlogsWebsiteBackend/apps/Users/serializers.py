from rest_framework import serializers
from .models import User
from apps.Blogs.models import Post
from apps.Blogs.serializers import PostSerializer


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.SerializerMethodField()

    def get_posts(self, request):
        qs = Post.objects.filter(status='APPROVED')
        serializer = PostSerializer(instance=qs, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = User
        fields = ('id', 'email', 'user_name', 'first_name', 'last_name', 'posts')
