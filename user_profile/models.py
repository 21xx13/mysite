from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class MainCycle(models.Model):
    user = models.OneToOneField(User, related_name='cycle', null=False, on_delete=models.CASCADE)
    coinsCount = models.IntegerField(default=0)
    clickPower = models.IntegerField(default=1)
    level = models.IntegerField(default=0)
    autoClickPower = models.IntegerField(default=0)

    def Click(self):
        self.coinsCount += self.clickPower
        return self.check_level()

    def check_level(self):
        if (self.coinsCount > (self.level**2+1)*1000): 
            self.level += 1
            boost_type = 1
            if self.level % 3 == 2:
                boost_type = 0
            boost = Boost(mainCycle = self, level = self.level, boost_type = boost_type)
            boost.save()
            return True
        return False    


class Boost(models.Model):
    mainCycle = models.ForeignKey(MainCycle, related_name='boosts', null=False, on_delete=models.CASCADE)
    power = models.IntegerField(default=3)
    level = models.IntegerField(default=0, null=False)
    price = models.IntegerField(default=10)
    level_boost = models.IntegerField(default=0, null=False)
    boost_type = models.IntegerField(default=1)

    def upgrade(self):
        if self.price <= self.mainCycle.coinsCount:
            self.level_boost += 1
            self.mainCycle.coinsCount -= self.price 

            if self.boost_type == 1:
                self.mainCycle.clickPower += self.power
                self.price += self.power * self.level_boost * 10
                if self.level_boost % 3 == 0:
                    self.power += 1 
            else:
                self.mainCycle.autoClickPower += self.power
                self.price += self.power * self.level_boost * 50  
                self.power += 1 
                  
            self.mainCycle.save()    
        return (self.mainCycle, self.level, self.price, self.power, self.level_boost)

    def update_coins_count(self, current_coins_count):
        self.mainCycle.coinsCount += current_coins_count
        return self.mainCycle    
        
        
              
        
