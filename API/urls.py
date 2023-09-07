from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
