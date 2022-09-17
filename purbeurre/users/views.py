from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from . import forms
from django.contrib.auth.decorators import login_required


# Create your views here.


def logout_user(request):
    logout(request)
    return redirect("login")


def login_page(request):
    form = forms.LoginForm()
    message = ""
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                message = "Identifiants invalides."
    return render(
        request, "users/login.html", context={"form": form, "message": message}
    )


def signup_page(request):
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "users/signup.html", context={"form": form})

@login_required
def profile_page(request):
    
    return render(
        request,
        "users/profile.html",
    )
    
def legal_notices(request):
    return render(
        request,
        "users/legal_notices.html",
    )