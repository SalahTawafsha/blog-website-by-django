from django.urls import path

from . import views

urlpatterns = [
    path("", views.user_log_in, name="index"),
    path("users/add-user/", views.user_register, name="add_user"),
    path("users/log-out/", views.log_out, name="log_out"),
    path('like_post/', views.like_post, name='like_post'),
    path('dislike_post/', views.dislike_post, name='dislike_post'),
    path('subscribe/', views.subscribe, name='subscribe'),

]
