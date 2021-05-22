from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserForm
from .models import MainCycle, Boost
from .serializers import UserSerializer, UserSerializerDetail, CycleSerializer, CycleSerializerDetail, BoostSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
import services

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
    queryset = Boost
    serializer_class = BoostSerializer
    def get_queryset(self):
        return Boost.objects.filter(mainCycle=self.kwargs['mainCycle'])

@api_view(['POST'])
def buyBoost(request):
    click_power, coins_count, level, price, power, level_boost, boosts = services.clicker_services.buyBoost(request)
    return Response({'clickPower': click_power,
                     'coinsCount': coins_count,
                     'level': level,
                     'price': price,
                     'power': power,
                     'level_boost': level_boost,
                     'boosts': boosts})

@api_view(['GET'])
def callClick(request):
    data = services.clicker_services.callClick(request)
    return Response(data)




# def upgradeBoost(request): 
#     mainCycle = MainCycle.objects.filter(user=request.user)[0] 
#     boost = Boost.objects.filter(mainCycle=mainCycle)[0]
#     boost.mainCycle = mainCycle
#     boost.Upgrade()
#     boost.save()
#     return HttpResponse(mainCycle.clickPower)    