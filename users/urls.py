from django.urls import path

from . import views

urlpatterns = [
    path("", views.user_log_in, name="index"),
    path("users/add-user/", views.user_register, name="add_user"),
    path("users/log-out/", views.log_out, name="log_out")

]
