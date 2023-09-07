from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, redirect


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


# Create your views here.
class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


def user_register(request):
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


def user_log_in(request):
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


def log_out(request):
    logout(request)
    return redirect("index")