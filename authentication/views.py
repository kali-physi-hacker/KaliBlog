from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_method 
from django.contrib.auth import logout as logout_method
from django.urls import reverse 
from django.contrib import messages

from authentication.forms import UserLoginForm, UserRegistrationForm


def login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            if user:    
                login_method(request, user)
                return redirect(reverse("home"))
            else:
                messages.error(request, "Invalid Username or Password")
                return redirect(reverse("authentication:login"))
        else:
            import pdb; pdb.set_trace()         # For Development Purposes

    template = "authentication/login.html"
    form = UserLoginForm()
    context = {"form": form}
    return render(request, template, context)


def logout(request):
    logout_method(request)
    return redirect(reverse("home"))


    # 024266496


def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("home"))
        else:
            messages.error(request, form.errors)
            
    template = "authentication/signup.html"
    form = UserRegistrationForm()
    context = {"form": form}
    return render(request, template, context)