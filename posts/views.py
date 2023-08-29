from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.utils import timezone
import datetime

from .models import Post, Comment


# Create your views here.
def index(request):
    # use my manager to get published posts
    published_posts = Post.objects.published_posts()
    paginator = Paginator(published_posts, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "posts/index.html", context)


def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "posts/postDetail.html", {"post": post})


def create_post(request):
    return render(request, "posts/create_post.html", {})


def create(request):
    post = Post(title=request.POST["title"], body=request.POST["body"], author=request.POST["author"])
    post.save()
    return HttpResponseRedirect(reverse("index"))


def comment_action(request):
    last_comments = Comment.objects.filter(email=request.POST["email"]).order_by("-updated")
    if last_comments and last_comments[0].updated > timezone.now() - datetime.timedelta(seconds=30):
        return render(request, "posts/postDetail.html", {
            "post": Post.objects.get(id=request.POST["post_id"]),
            "error_message": f"You can't comment twice in 30 seconds.",
            "expand_comment": True,
        })
    else:
        comment = Comment(post_id=request.POST["post_id"], user_name=request.POST["name"],
                          body=request.POST["body"], email=request.POST["email"])
        comment.save()
        return render(request, "posts/postDetail.html", {
            "post": Post.objects.get(id=request.POST["post_id"]),
            "expand_comment": True,
        })
