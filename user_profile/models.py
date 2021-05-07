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
    power = models.IntegerField(default=1)
    level = models.IntegerField(default=1)
    price = models.IntegerField(default=10)

    def Upgrade(self):
        self.power = 3
        self.mainCycle.clickPower += self.power
        self.mainCycle.coinsCount -= self.price
        self.price += 20
        self.level += 1
