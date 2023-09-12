from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from posts.models import Post, Comment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
