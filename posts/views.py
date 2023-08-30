from django.core.paginator import Paginator
from django import forms
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Post, Comment

PAGE_SIZE = 3


class CreatePostForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    author = forms.CharField(label="Author", max_length=30)
    body = forms.CharField(label="Body", max_length=2000, widget=forms.Textarea)


class AddCommentForm(forms.Form):
    name = forms.CharField(label="Name", max_length=30)
    email = forms.EmailField(label="Email", max_length=30)
    body = forms.CharField(label="Body", max_length=2000, widget=forms.Textarea)


# Create your views here.
def index(request):
    # use my manager to get published posts
    published_posts = Post.published_objects.all()
    paginator = Paginator(published_posts, PAGE_SIZE)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "posts/index.html", context)


def post_details(request, slug):
    form = AddCommentForm()
    post = get_object_or_404(Post, slug=slug)
    return render(request, "posts/postDetail.html", {"post": post, "form": form})


def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            author = form.cleaned_data["author"]
            body = form.cleaned_data["body"]

            post = Post(title=title, author=author, body=body)
            post.save()
            return HttpResponseRedirect(reverse("post_details", args=(post.slug,)))
    else:
        form = CreatePostForm()

    return render(request, "posts/create_post.html", {'form': form})


def comment_action(request):
    form = AddCommentForm(request.POST)
    if form.is_valid():
        post_id = request.POST["post_id"]
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        body = form.cleaned_data["body"]

        comment = Comment(post_id=post_id, user_name=name,
                          body=body, email=email)

        if comment.is_there_comment_in_recent_30_sec():
            return render(request, "posts/postDetail.html", {
                "post": Post.published_objects.get(id=request.POST["post_id"]),
                "error_message": f"You can't comment twice in 30 seconds.",
                "expand_comment": True,
                "form": form,
            })

        comment.save()
        return render(request, "posts/postDetail.html", {
            "post": Post.published_objects.get(id=request.POST["post_id"]),
            "expand_comment": True,
            "form": AddCommentForm(),
        })
    else:
        raise Http404("Question does not exist")
