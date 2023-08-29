from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new-post/", views.create_post, name="create_post"),
    path("create/", views.create, name="create"),
    path("comment-action/", views.comment_action, name="comment_action"),
    path("<slug:slug>/", views.post_details, name="post_details"),
]
