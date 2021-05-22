from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from user_profile.forms import UserForm
from user_profile.models import MainCycle, Boost


def user_login(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            return (True, 'index', {})
        else:
            return (False, 'login.html', {'invalid':True})
    else:
        return (False, 'login.html', {'invalid':False})


def user_logout(request):
    logout(request)
    return ('login')


def user_registration(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            mainCycle = MainCycle()
            boost = Boost(mainCycle = mainCycle, level = 0)
            mainCycle.user = user
            mainCycle.save()
            boost.save()
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            return (True, 'index', {})

        else:
            return (False, 'registration.html', {'invalid':True, 'form': form})
    else:
        form = UserForm()
        return (False, 'registration.html', {'invalid':False, 'form': form})