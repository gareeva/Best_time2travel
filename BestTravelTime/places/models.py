from django.db import models
from django.db.models.functions import Concat
from datetime import date

# Create your models here.
class Country(models.Model):
    short_name = models.CharField(max_length=1000, default='none')
    country_name = models.CharField(max_length=1000, default='none')
    def __str__(self):
        return self.country_name

class City(models.Model):
    city_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=1000)
    #region_name = models.ForeignKey(Region, on_delete=models.CASCADE)
    def __str__(self):
        return self.city_name

class Indicators_byMonth(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    month = models.IntegerField()
    month_score = models.IntegerField(default = 0)

    # icon  = models.CharField(max_length=200, default = None)

    average_apparent_temp = models.FloatField(null=True) #Degrees Celsius.
    average_humidity = models.FloatField(null=True)
    # moonphase_cycles =
    average_precipitation_intencity = models.FloatField(null=True)
    average_precipitation_accumulation = models.FloatField(null=True)

    wet_days_count = models.IntegerField()
    count_of_rain_days = models.IntegerField()
    count_of_snow_days = models.IntegerField()
    count_of_sleet_days = models.IntegerField()
    count_of_cloudy_days = models.IntegerField()
    count_of_clear_days = models.IntegerField()
    count_of_wind_days = models.IntegerField()
    count_of_fog_days = models.IntegerField()

    pressure = models.FloatField(null=True)
    average_wind_speed = models.FloatField(null=True)
    average_visibility = models.FloatField(null=True)

    def __str__(self):
        longname = str(self.city)+ "_" + str(self.month) + "_" + str(self.month_score)
        longname = longname + ":" + str(self.average_apparent_temp) + ";" + str(self.average_humidity) + ";" + str(self.average_precipitation_intencity) + ";" + str(self.average_precipitation_accumulation) + ";" + str(self.average_wind_speed) + ";" + str(self.average_visibility)
        return longname

class Indicators_byDay(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    # day = models.IntegerField(default=-1)
    # month = models.IntegerField(default=-1)
    date = models.DateField(default = date.today)
    day_score = models.IntegerField(default = 0)
    icon  = models.CharField(max_length=200, default = None)
    apparent_temp_high = models.FloatField(null=True) #Degrees Celsius.
    apparent_temp_low = models.FloatField(null=True) #Degrees Celsius.
    apparent_temp_max = models.FloatField(null=True) #Degrees Celsius.
    apparent_temp_min = models.FloatField(null=True) #Degrees Celsius.
    humidity = models.FloatField(null=True) #The relative humidity, between 0 and 1, inclusive.
    moonphase = models.FloatField(null=True) #a value of 0 corresponds to a new moon, 0.25 to a first quarter moon, 0.5 to a full moon, and 0.75 to a last quarter moon
    temp_max = models.FloatField(null=True) #Degrees Celsius.
    temp_min = models.FloatField(null=True) #Degrees Celsius.

    precip_intencity_max = models.FloatField(null=True) #Millimeters per hour.
    precip_accumulation_max = models.FloatField(null=True) #Centimeters
    precip_type = models.CharField(max_length=100, null=True) #values: "rain", "snow", or "sleet" if precip_intencity exists
    wind_speed = models.FloatField(null=True) #Meters per second.
    visibility = models.FloatField(null=True) #Kilometers
    pressure = models.FloatField(null=True) #millibars

    def __str__(self):
        longname = str(self.city) + str(self.date)
        return longname