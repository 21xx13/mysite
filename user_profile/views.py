from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, NoteForm
from .models import Note
from .serializers import UserSerializer, UserSerializerDetail
from rest_framework import generics

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerDetail
    

def index(request):
    user = User.objects.filter(id=request.user.id)
    
    if len(user) != 0:
        notes_list = Note.objects.filter(author = user[0].username)
        form = NoteForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            Note.objects.create(title=title, text=text, author = user[0].username)
        else: 
            form = NoteForm()
        return render(request, 'index.html', {'user':user[0], 'form_note': form, 'notes_list': notes_list})
    else:
        return redirect('login')

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'invalid':True})
    else:
        return render(request, 'login.html', {'invalid':False})


def user_logout(request):
    logout(request)
    return redirect('login')


def user_registration(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            existing_user = User.objects.filter(username=username)
            if len(existing_user) == 0:
                password = form.cleaned_data['password']
                user = User.objects.create_user(username, '', password)
                user.save()
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'registration.html', {'invalid':True, 'form': form})
    else:
        form = UserForm()
        return render(request, 'registration.html', {'invalid':False, 'form': form})
