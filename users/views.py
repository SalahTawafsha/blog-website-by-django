from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import OperationalError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from posts.models import Post


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


# Create your views here.
class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


def user_register(request):
    try:
        if request.method == "GET":
            form = AddUserForm()
            return render(request, "users/add_user.html", {"form": form})

        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect("index")
        else:
            return render(request, "users/add_user.html", {"form": form})
    except OperationalError:
        return render(request, "database_error.html")


def user_log_in(request):
    try:
        if request.user.is_authenticated:
            return redirect("posts")

        if request.method == "GET":
            form = LoginForm()
            return render(request, "users/log_in.html", {"form": form})

        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("posts")

        return render(request, "users/log_in.html", {"form": form})
    except OperationalError:
        return render(request, "database_error.html")


def log_out(request):
    try:
        logout(request)
        return redirect("index")
    except OperationalError:
        return render(request, "database_error.html")


def like_post(request):
    try:
        post = Post.objects.get(pk=request.POST["post_id"])
        request.user.usertracking.like_post(post)
        return HttpResponseRedirect(reverse("post_details", args=(post.slug,)))
    except OperationalError:
        return render(request, "database_error.html")


def dislike_post(request):
    try:
        post = Post.objects.get(pk=request.POST["post_id"])
        request.user.usertracking.dislike_post(post)
        return HttpResponseRedirect(reverse("post_details", args=(post.slug,)))
    except OperationalError:
        return render(request, "database_error.html")


def subscribe(request):
    try:
        user = User.objects.get(pk=request.POST["user_id"])
        request.user.usertracking.subscribe(user)
        return HttpResponseRedirect(reverse("post_details", args=(request.POST["post_slug"],)))
    except OperationalError:
        return render(request, "database_error.html")
