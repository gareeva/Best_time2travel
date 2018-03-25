from django.db import models
from django.db.models.functions import Concat
from datetime import date

# Create your models here.
class Country(models.Model):
    short_name = models.CharField(max_length=1000, default='none')
    country_name = models.CharField(max_length=1000, default='none')
    def __str__(self):
        return self.country_name

# class Region(models.Model):
#     name = models.CharField(max_length=1000, default='none')
#     region_country = models.ForeignKey(Country, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.name

class City(models.Model):
    city_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=1000)
    #region_name = models.ForeignKey(Region, on_delete=models.CASCADE)
    def __str__(self):
        return self.city_name

class Indicators_byMonth(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    month = models.IntegerField(default=0)
    month_score = models.IntegerField(default=0)

    # icon  = models.CharField(max_length=200, default = None)

    average_apparent_temp = models.FloatField(default=0) #Degrees Celsius.
    average_humidity = models.FloatField(default=0)
    # moonphase_cycles =
    average_precipitation_intencity = models.FloatField(default=0)
    average_precipitation_accumulation = models.FloatField(default=0)

    wet_days_count = models.IntegerField(default=0)
    count_of_rain_days = models.IntegerField(default=0)
    count_of_snow_days = models.IntegerField(default=0)
    count_of_sleet_days = models.IntegerField(default=0)
    count_of_cloudy_days = models.IntegerField(default=0)
    count_of_clear_days = models.IntegerField(default=0)
    count_of_wind_days = models.IntegerField(default=0)
    count_of_fog_days = models.IntegerField(default=0)

    pressure = models.FloatField(default=0)
    average_wind_speed = models.FloatField(default=0)
    average_visibility = models.FloatField(default=0)

    def __str__(self):
        longname = str(self.city)
        longname = longname + str(self.month)
        return longname

class Indicators_byDay(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    day = models.IntegerField(default=-1)
    month = models.IntegerField(default=-1)
    date = models.DateField(default = date.today)
    icon  = models.CharField(max_length=200, default = None)
    apparent_temp_high = models.FloatField(default=0) #Degrees Celsius.
    apparent_temp_low = models.FloatField(default=0) #Degrees Celsius.
    apparent_temp_max = models.FloatField(default=0) #Degrees Celsius.
    apparent_temp_min = models.FloatField(default=0) #Degrees Celsius.
    humidity = models.FloatField(default=0) #The relative humidity, between 0 and 1, inclusive.
    moonphase = models.FloatField(default=-1) #a value of 0 corresponds to a new moon, 0.25 to a first quarter moon, 0.5 to a full moon, and 0.75 to a last quarter moon
    temp_max = models.FloatField(default=0) #Degrees Celsius.
    temp_min = models.FloatField(default=0) #Degrees Celsius.

    precip_intencity_max = models.FloatField(default=0) #Millimeters per hour.
    precip_accumulation_max = models.FloatField(default=0) #Centimeters
    precip_type = models.CharField(max_length=100) #values: "rain", "snow", or "sleet" if precip_intencity exists
    wind_speed = models.FloatField(default=0) #Meters per second.
    visibility = models.FloatField(default=0) #Kilometers
    pressure = models.FloatField(default=0) #millibars

    def __str__(self):
        longname = str(self.city)
        longname = longname + str(self.day) + str(self.month)
        return longname