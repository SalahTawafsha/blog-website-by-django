from django.core.paginator import Paginator
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .models import Post, Comment

PAGE_SIZE = 3


class AddPostForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    body = forms.CharField(label="Body", max_length=2000, widget=forms.Textarea)


class AddCommentForm(forms.Form):
    name = forms.CharField(label="Name", max_length=30)
    email = forms.EmailField(label="Email", max_length=30)
    body = forms.CharField(label="Body", max_length=2000, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        initial = kwargs.get('initial', {})
        if 'name' in initial:
            self.fields['name'].widget = forms.HiddenInput()
        if 'email' in initial:
            self.fields['email'].widget = forms.HiddenInput()


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
    if request.user.is_authenticated:
        user = request.user
        form = AddCommentForm(initial={"name": user.username, "email": user.email})
        form.fields["name"].widget = forms.HiddenInput()
        form.fields["email"].widget = forms.HiddenInput()
    else:
        form = AddCommentForm()

    post = get_object_or_404(Post, slug=slug)
    return render(request, "posts/postDetail.html", {"post": post, "form": form})


def add_comment(request):
    if request.method == "POST":

        if request.user.is_authenticated:
            user = request.user
            form = AddCommentForm(request.POST, initial={"name": user.username, "email": user.email})
        else:
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

            if request.user.is_authenticated:
                user = request.user
                form = AddCommentForm(initial={"name": user.username, "email": user.email})
            else:
                form = AddCommentForm()
            return render(request, "posts/postDetail.html", {
                "post": Post.published_objects.get(id=request.POST["post_id"]),
                "expand_comment": True,
                "form": form,
            })
        else:
            return render(request, "posts/postDetail.html", {
                "post": Post.published_objects.get(id=request.POST["post_id"]),
                "expand_comment": True,
                "form": form,
            })

    if request.user.is_authenticated:
        user = request.user
        form = AddCommentForm(initial={"name": user.username, "email": user.email})
    else:
        form = AddCommentForm()

    return render(request, "posts/postDetail.html", {
        "post": Post.published_objects.get(id=request.POST["post_id"]),
        "expand_comment": True,
        "form": form,
    })


def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddPostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]
                author = request.user
                body = form.cleaned_data["body"]

                post = Post(title=title, author=author, body=body)
                post.save()
                return HttpResponseRedirect(reverse("post_details", args=(post.slug,)))
            else:
                return render(request, "posts/create_post.html", {'form': form})

        return render(request, "posts/create_post.html", {'form': AddPostForm()})
    else:
        return redirect("index")
