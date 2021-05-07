from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class MainCycle(models.Model):
    user = models.OneToOneField(User, related_name='cycle', null=False, on_delete=models.CASCADE)
    coinsCount = models.IntegerField(default=0)
    clickPower = models.IntegerField(default=1)
    def Click(self):
        self.coinsCount += self.clickPower

class Boost(models.Model):
    mainCycle = models.ForeignKey(MainCycle, related_name='boost', null=False, on_delete=models.CASCADE)
    power = models.IntegerField(default=3)
    level = models.IntegerField(default=0)
    price = models.IntegerField(default=10)

    def Upgrade(self):
        self.level += 1 
        self.mainCycle.coinsCount -= self.price 
        self.mainCycle.clickPower += self.power      
        if self.level < 3:
            self.power = 3
            self.price *= 5
        elif 2 < self.level < 5:
            self.power = 5
            self.price *= 4
        else: 
            self.power += 2
            self.price += 1000  
        
        
              
        
