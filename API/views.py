from django.contrib.auth.models import User, AnonymousUser
from django.db import IntegrityError, OperationalError
from django.db.models import Q
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

    def create(self, request, *args, **kwargs):
        try:
            if not request.POST.get("username", False) or not request.POST.get("email", False) \
                    or not request.POST.get("password", False):
                return Response(data={"message": "you must provide username, email and password"},
                                status=status.HTTP_400_BAD_REQUEST)
            User.objects.create(username=request.POST["username"], email=request.POST["email"],
                                password=request.POST["password"])

            return Response(data={"message": "User added successfully!"}, status=status.HTTP_200_OK)
        except OperationalError:
            return Response(data={"message": "The database server is currently unavailable."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)


class PostViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Posts to be viewed or edited."""
    queryset = Post.objects.all().filter(status="P").order_by('-created')
    serializer_class = PostSerializer
    # AnonymousPostPermission is allowing just GET
    # and AuthenticatedPostPermission is allowing all others for authenticated users
    permission_classes = (AnonymousPostPermission | AuthenticatedPostPermission,)

    def get_queryset(self, *args, **kwargs):
        try:
            if not isinstance(self.request.user, AnonymousUser):
                user = self.request.user
                return Post.objects.all().filter(Q(status="P") | Q(author=user)).order_by('-created')

            return self.queryset
        except OperationalError:
            return Response(data={"message": "The database server is currently unavailable."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def create(self, request, *args, **kwargs):
        try:
            if not request.POST.get("title", False) or not request.POST.get("body", False):
                return Response(data={"message": "title and body are required in data request"},
                                status=status.HTTP_400_BAD_REQUEST)

            user = Token.objects.get(key=request.auth.key).user
            Post.objects.create(title=request.POST["title"], author=user, body=request.POST["body"])

            return Response(data={"message": f"{request.POST['title']} added successfully!"}, status=status.HTTP_200_OK)
        except OperationalError:
            return Response(data={"message": "The database server is currently unavailable."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def update(self, request, *args, **kwargs):
        try:
            if not request.POST.get("title", False) or not request.POST.get("body", False):
                return Response(data={"message": "title and body are required in data request"},
                                status=status.HTTP_400_BAD_REQUEST)

            instance = self.get_object()

            user = Token.objects.get(key=request.auth.key).user
            if instance.author == user:
                instance.title = request.POST["title"]
                instance.body = request.POST["body"]
                instance.save()
                return Response(data={"message": "Post Updated successfully!!"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"message": "You are NOT the author of this post !!"},
                                status=status.HTTP_401_UNAUTHORIZED)
        except OperationalError:
            return Response(data={"message": "The database server is currently unavailable."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            user = Token.objects.get(key=request.auth.key).user
            if instance.author == user:
                super().destroy(request, *args, **kwargs)
                return Response(data={"message": "Deleted !!"},
                                status=status.HTTP_200_OK)
            else:
                return Response(data={"message": "You are NOT the author of this post !!"},
                                status=status.HTTP_400_BAD_REQUEST)
        except OperationalError:
            return Response(data={"message": "The database server is currently unavailable."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)


class CommentViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Comments to be viewed or edited."""
    queryset = Comment.objects.all().filter(isActive=True).order_by('-created')
    serializer_class = CommentSerializer
    # CommentPermission is just allowing GET and POST methods for all users
    permission_classes = (CommentPermission,)

    def create(self, request, *args, **kwargs):
        try:
            if not isinstance(request.user, AnonymousUser):
                if not request.POST.get("post_id", False) or not request.POST.get("body", False):
                    return Response(data={"message": "you must provide post_id and body"},
                                    status=status.HTTP_400_BAD_REQUEST)

                user = Token.objects.get(key=request.auth.key).user
                try:
                    comment = Comment(post_id=request.POST["post_id"], user_name=user.username,
                                      email=user.email, body=request.POST["body"])
                    comment.save()
                    return Response(data={"message": f"{request.POST['body']} added Success!"},
                                    status=status.HTTP_200_OK)
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

        except OperationalError:
            return Response(data={"message": "The database server is currently unavailable."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
