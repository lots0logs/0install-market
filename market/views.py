from django.shortcuts import render
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from parsley.decorators import parsleyfy

from market.forms import LoginForm

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = parsleyfy(UserCreationForm())

    return render(request, "registration/register.html", {
        'form': form,
    })

def loginview(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    error = False
    # TODO: Replace with built in authentication form?
    form = LoginForm()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                error = 'This account is inactive.'
        else:
            error = 'Username or password incorrect.'

    return render(request, "registration/login.html", {
        'error': error,
        'form' : form,
    })

def logoutview(request):
    logout(request)
    return HttpResponseRedirect("/")

def home(request):
  return render(request, "home.html")
