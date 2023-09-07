from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from posts.models import Post, Comment


def encrypt_function(string):
    encrypt_string = ""
    for char in string:
        encrypt_string += chr(ord(char) + 2)

    return encrypt_string


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def to_representation(self, instance):
        # Retrieve the original representation of the instance
        original_representation = super().to_representation(instance)

        # Encrypt the password field (replace 'password' with the actual field name)
        original_representation['password'] = encrypt_function(original_representation['password'])

        return original_representation


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
