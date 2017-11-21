from django.db import models
from django.db.models.functions import Concat

# Create your models here.
class Country(models.Model):
    short_name = models.CharField(max_length=1000, default='none')
    country_name = models.CharField(max_length=1000, default='none')
    def __str__(self):
        return self.country_name

class City(models.Model):
    city_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.city_name

class Indicators(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    month = models.DateTimeField('tracked month')
    temperature = models.IntegerField(default=0)
    precipitation = models.IntegerField(default=0)

    def __str__(self):
        longname = str(self.city)
        longname = longname + str(self.month)
        return longname