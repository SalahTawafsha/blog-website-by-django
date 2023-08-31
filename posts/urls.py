from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="posts"),
    path("new-post/", views.add_post, name="create_post"),
    path("comment-action/", views.add_comment, name="comment_action"),
    path("post-details/<slug:slug>/", views.post_details, name="post_details"),
]
