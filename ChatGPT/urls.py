from django.urls import path
from . import views

urlpatterns = [
    path("create-post/", views.generate_post, name="generate_post"),
    path("summarize-post/", views.summarize_post, name="summarize_post"),
    path("fix-post-grammar/", views.fix_post_grammar, name="fix_post_grammar"),

]
