from django.contrib.auth.models import User
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
def buy_boost(request):
    click_power, coins_count, level, price, power, level_boost, boosts = services.clicker_services.buyBoost(request)
    return Response({'clickPower': click_power,
                     'coinsCount': coins_count,
                     'level': level,
                     'price': price,
                     'power': power,
                     'level_boost': level_boost,
                     'boosts': boosts})

@api_view(['GET'])
def call_click(request):
    data = services.clicker_services.callClick(request)
    return Response(data)
  