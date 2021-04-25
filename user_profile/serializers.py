from rest_framework import serializers
from .models import UserData, MainCycle

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['id']

class UserSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['id', 'username', 'password']   

class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCycle
        fields = ['id']  

class CycleSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = MainCycle
        fields = ['id', 'user', 'coinsCount', 'clickPower']                      