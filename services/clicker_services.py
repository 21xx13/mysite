from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_profile.models import MainCycle, Boost
from rest_framework import generics
from user_profile.serializers import UserSerializer, UserSerializerDetail, CycleSerializer, CycleSerializerDetail, BoostSerializer


def main_page(request):
    user = User.objects.filter(id=request.user.id)
    if len(user) != 0:
        mainCycle = MainCycle.objects.get(user=request.user)
        return (False, 'index.html', {'user':user[0], 'mainCycle':mainCycle})
    else:
        return (True, 'login', {})
    

def callClick(request):
    mainCycle = MainCycle.objects.get(user=request.user)
    mainCycle.Click()
    boosts_query = Boost.objects.filter(mainCycle=mainCycle)
    boosts = BoostSerializer(boosts_query, many=True).data
    mainCycle.save()
    return ({"coinsCount": mainCycle.coinsCount,
            "cycleLevel": mainCycle.level,
            "boosts": boosts})

def buyBoost(request):
    boost_level = request.data['boost_level']
    cycle = MainCycle.objects.get(user=request.user)
    boosts_query = Boost.objects.filter(mainCycle=cycle)   
    boost = Boost.objects.get_or_create(mainCycle=cycle, level=boost_level)[0]   
    click_power, coins_count, level, price, power, level_boost = boost.upgrade()
    boost.save()
    boosts = BoostSerializer(boosts_query, many=True).data
    return (click_power, coins_count, level, price, power, level_boost, boosts)


