from django.contrib import messages
from django.core.paginator import Paginator
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from ChatGPT.GPT import GPT
from users.models import MAX_ALLOWED_POST_POSTS_IN_DAY, MAX_ALLOWED_READ_POSTS_IN_DAY, DAYS_OF_BLOCK
from .models import Post, Comment, ALLOWED_NUM_OF_CENSORED_WORDS

PAGE_SIZE = 4


class PostForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    body = forms.CharField(label="Body", max_length=5000,
                           widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))


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


def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix


# Create your views here.
def index(request):
    # use my manager to get published posts
    published_posts = Post.published_objects.all().order_by("-updated")
    paginator = Paginator(published_posts, PAGE_SIZE)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }

    if request.user.is_authenticated:
        if not request.user.usertracking.is_can_read_post():
            messages.error(request, f"You can't read posts since you reach max allowed"
                                    f" posts in day that is {MAX_ALLOWED_READ_POSTS_IN_DAY}")

        subscriptions = request.user.usertracking.subscriptions.all()
        subscriptions_posts = {}
        for subscriber in subscriptions:
            subscriber_posts = subscriber.post_set.all()

            if subscriber_posts:
                unread_posts = []
                for subscriber_post in subscriber_posts:
                    if subscriber_post not in request.user.usertracking.read_posts.all():
                        unread_posts.append(subscriber_post)

                if unread_posts:
                    subscriptions_posts[subscriber.username] = unread_posts

        context["subscriptions_posts"] = subscriptions_posts

    return render(request, "posts/index.html", context)


def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]

            post.title = title
            post.body = body
            post.save()

    if request.GET.get("summary"):
        post.body = GPT.summarize_post(post.body)

    if request.GET.get("grammar"):
        post.body = GPT.fix_grammar(post.body)

    if request.user.is_authenticated:
        user = request.user
        if post.author != user and not user.usertracking.is_can_read_post():
            return redirect("index")

        if request.GET.get("edit") and post.author == request.user and not post.author.usertracking.is_blocked():
            form = PostForm(initial={"title": post.title, "body": post.body})

            return render(request, "posts/postDetail.html", {"post": post, 'form': form, "edit": True})

        if post.author != user:
            user.usertracking.increment_read_posts(post)

        form = AddCommentForm(initial={"name": user.username, "email": user.email})
        form.fields["name"].widget = forms.HiddenInput()
        form.fields["email"].widget = forms.HiddenInput()
    else:
        form = AddCommentForm()

    context = {"post": post, "form": form}
    if request.user.is_authenticated and request.user != post.author:
        context["current_viewing_number"] = ordinal(request.user.usertracking.read_posts_num)
        context["remaining_viewing_number"] = MAX_ALLOWED_READ_POSTS_IN_DAY - request.user.usertracking.read_posts_num

    return render(request, "posts/postDetail.html", context)


def add_comment(request):
    if request.method == "POST":

        if request.user.is_authenticated:
            user = request.user
            form = AddCommentForm(request.POST, initial={"name": user.username, "email": user.email})
        else:
            form = AddCommentForm(request.POST)

        if form.is_valid():

            comment = Comment(post_id=request.POST["post_id"], user_name=form.cleaned_data["name"],
                              email=form.cleaned_data["email"], body=form.cleaned_data["body"])

            if comment.is_there_comment_in_recent_30_sec():
                messages.error(request, f"You can't comment twice in 30 seconds.")
                return render(request, "posts/postDetail.html", {
                    "post": Post.published_objects.get(id=request.POST["post_id"]),
                    "expand_comment": True,
                    "form": form,
                })

            if request.user.is_authenticated and request.user.usertracking.is_blocked():
                messages.error(request, f"You can't comment Since you are blocked "
                                        f"because you post a lot of censored words.")
                return render(request, "posts/postDetail.html", {
                    "post": Post.published_objects.get(id=request.POST["post_id"]),
                    "expand_comment": True,
                    "form": form,
                })

            if comment.save():
                messages.warning(request,
                                 f"You get a warning since you use"
                                 f" {ALLOWED_NUM_OF_CENSORED_WORDS} or more bad words.")

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
            form = PostForm(request.POST)

            if request.user.usertracking.is_blocked():
                messages.error(request, f"You can't add post Since you are blocked for {DAYS_OF_BLOCK}"
                                        f"because you post a lot of censored words."
                                        f"date of block is {request.user.usertracking.date_of_block}")
                return render(request, "posts/create_post.html", {
                    "form": form,
                })

            if not request.user.usertracking.is_can_post_post():
                messages.error(request, f"You can't add post Since you reach "
                                        f"max number of posts in day that is {MAX_ALLOWED_POST_POSTS_IN_DAY}.")
                return render(request, "posts/create_post.html", {
                    "form": form,
                })

            if form.is_valid():
                title = form.cleaned_data["title"]
                author = request.user
                body = form.cleaned_data["body"]

                post = Post(title=title, author=author, body=body)
                if post.save():
                    messages.warning(request,
                                     f"You get a warning since you use"
                                     f" {ALLOWED_NUM_OF_CENSORED_WORDS} or more bad words.")

                request.user.usertracking.increment_post_posts()
                return HttpResponseRedirect(reverse("post_details", args=(post.slug,)))
            else:
                return render(request, "posts/create_post.html", {'form': form})

        return render(request, "posts/create_post.html", {'form': PostForm()})
    else:
        return redirect("index")
