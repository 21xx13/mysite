from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserForm
from .models import MainCycle, Boost
from .serializers import UserSerializer, UserSerializerDetail, CycleSerializer, CycleSerializerDetail, BoostSerializer, BoostSerializerDetail
from rest_framework import generics

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerDetail

class CycleList(generics.ListAPIView):
    queryset = MainCycle.objects.all()
    serializer_class = CycleSerializer

class CycleDetail(generics.RetrieveAPIView):
    queryset = MainCycle.objects.all()
    serializer_class = CycleSerializerDetail

class BoostList(generics.ListAPIView):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer

class BoostDetail(generics.RetrieveAPIView):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializerDetail

def callClick(request):
    mainCycle = MainCycle.objects.filter(user=request.user)[0]
    mainCycle.Click()
    mainCycle.save()
    return HttpResponse(mainCycle.coinsCount)

def buyBoost(request):
    mainCycle = MainCycle.objects.filter(user=request.user)[0]
    boost = Boost()
    boost.mainCycle = mainCycle
    boost.Upgrade()
    boost.save()
    mainCycle.save()
    return HttpResponse(mainCycle.clickPower)


def upgradeBoost(request): 
    mainCycle = MainCycle.objects.filter(user=request.user)[0] 
    boost = Boost.objects.filter(mainCycle=mainCycle)[0]
    boost.mainCycle = mainCycle
    boost.Upgrade()
    boost.save()
    mainCycle.save()
    return HttpResponse(mainCycle.clickPower)    


