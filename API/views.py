from django.contrib.auth.models import User, AnonymousUser
from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .permitions import (UserPermission, AnonymousPostPermission,
                         AuthenticatedPostPermission, CommentPermission)
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from posts.models import Post, Comment


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited."""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # user permission is an authenticated permission
    # that just allow GET, POST, PUT and DELETE methods
    permission_classes = [UserPermission]


class PostViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Posts to be viewed or edited."""
    queryset = Post.objects.all().order_by('-created')
    serializer_class = PostSerializer
    # AnonymousPostPermission is allowing just GET and POST
    # and AuthenticatedPostPermission is allowing all others for authenticated users
    permission_classes = (AnonymousPostPermission | AuthenticatedPostPermission,)

    def create(self, request, *args, **kwargs):
        if not request.POST.get("title", False) or not request.POST.get("body", False):
            return Response(data={"message": "title and body are required in data request"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = Token.objects.get(key=request.auth.key).user
        post = Post(title=request.POST["title"], author=user, body=request.POST["body"])
        post.save()
        return Response(data={"message": "Added Success!"}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if not request.POST.get("title", False) or not request.POST.get("body", False):
            return Response(data={"message": "title and body are required in data request"},
                            status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()

        user = Token.objects.get(key=request.auth.key).user
        if instance.author == user:
            instance.title = request.POST["title"]
            instance.body = request.POST["body"]
            instance.save()
            return Response(data={"message": "Updated !!"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "You are NOT the author of this post !!"},
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        user = Token.objects.get(key=request.auth.key).user
        if instance.author == user:
            super().destroy(request, *args, **kwargs)
            return Response(data={"message": "Deleted !!"},
                            status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "You are NOT the author of this post !!"},
                            status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Comments to be viewed or edited."""
    queryset = Comment.objects.all().order_by('-created')
    serializer_class = CommentSerializer
    # CommentPermission is just allowing GET, POST and DELETE methods for all users
    permission_classes = (CommentPermission,)

    def create(self, request, *args, **kwargs):
        if not isinstance(request.user, AnonymousUser):
            if not request.POST.get("post_id", False) or not request.POST.get("body", False):
                return Response(data={"message": "you must provide post_id and body"},
                                status=status.HTTP_400_BAD_REQUEST)

            user = Token.objects.get(key=request.auth.key).user
            try:
                comment = Comment(post_id=request.POST["post_id"], user_name=user.username,
                                  email=user.email, body=request.POST["body"])
                comment.save()
                return Response(data={"message": "Added Success!"}, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response(data={"message": "Post NOT exist!"}, status=status.HTTP_404_NOT_FOUND)

        if not request.POST.get("post_id", False) or not request.POST.get("body", False) \
                or not request.POST.get("email", False) or not request.POST.get("user_name", False):
            return Response(data={"message": "you must provide post_id, user_name, email and body"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            comment = Comment(post_id=request.POST["post_id"], user_name=request.POST["user_name"],
                              email=request.POST["email"], body=request.POST["body"])
            comment.save()
            return Response(data={"message": "Added Success!"}, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(data={"message": "Post NOT exist!"}, status=status.HTTP_404_NOT_FOUND)
