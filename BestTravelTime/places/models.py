from django.db import models

# Create your models here.

class Country(models.Model):
    country_name = models.CharField(max_length=1000)

class Indicators(models.Model):
    month = models.DateTimeField('tracked month')
    temperature = models.IntegerField(default=0)
    precipitation = models.IntegerField(default=0)

class City(models.Model):
    city_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=1000)
    indicator = models.ForeignKey(Indicators, on_delete=models.CASCADE)