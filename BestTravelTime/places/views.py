from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.template import loader

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
import requests
import json
import time, datetime

from .models import City, Indicators_byMonth, Country



# Create your views here.
def index(request):
    return render(request, 'places/index.html')

def placeenterform(request):
    return HttpResponse("enter here the city to visit!")

def timeenterform(request):
    return HttpResponse("enter here the holiday time!")

#def placedetails(request, city_id):
def placedetails(request):
    entered_city= request.POST.get('placename', False);
    #print(entered_city)
    required_city = City.objects.get(city_name = entered_city)

    place_info = []
    place_indicators = Indicators_byMonth.objects.all()
    for indicator in place_indicators:
        print(indicator)
        #if (3 == 3):
        if (indicator.city_id == required_city.id):
            place_info.append(indicator)

    context = {
        'place_name' : str(entered_city),
        'place_info' : place_info,
        'error_message' : "No such a city! Please enter another one!",
    }

    return HttpResponse(test_get_info_from_weatheronline(entered_city))
    #change the variables when cleaned
    #return render(request, 'places/city_details.html', context)

    #change to id later! Because you will need to automate the entering


#require the number of the month for a datetime!
def placestop(request):
    # datetime entered??
    places_top = []
    places_top = get_indicator_by_month()

    #change when you fix datetime in db!!!
    #places_top = Indicators.objects.filter(datetime = '2017-10-16 18:24:04.000000')

    new_city_list = []
    new_city_list = get_city_list(places_top)
    context = {
        'places_top' : new_city_list,
    }
    #return render(request, 'places/index.html', context)
    return render(request, 'places/places_top.html', context)

def get_indicator_by_month():
    places_top = []
    all_indicators = Indicators_byMonth.objects.all()

    for indicator in all_indicators:
        print(indicator)
        #ind.month = str(ind.month)
        #change when you fix datetime in db!!!
        if (str(indicator.month) == '2017-10-16 00:00:00+00:00'):
            places_top.append(indicator)
    return places_top

def get_city_list(places_top):
    new_city_list = []
    for indicator in places_top:
        if (City.objects.get(id = indicator.city_id)):
            city = City.objects.get(id = indicator.city_id)
            new_city_list.append(city)
    return new_city_list

# def test_get_info_from_weatheronline(cityname):
#     request_url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx?key=94105f4779354c0fa5372815171510&q='
#     #request_url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx?key=94105f4779354c0fa5372815171510&q=Moscow&format=json'
#     request_url = request_url + cityname
#     request_url = request_url + '&format=json'

#     response = requests.get(request_url)
#     response_json = response.json()

#     #decoded = json.loads(response_json)

#     monthAverages = response_json['data']['ClimateAverages'][0]['month']
#     string = ""
#     for month in monthAverages:
#         #print(month)
#         string = string + str(month)

#     #print(response_json)

#     #print (request_url)
#     return string


def get_city_coordinates(cityname):
    request_url =  "https://maps.googleapis.com/maps/api/geocode/json?address="
    request_url = request_url + cityname + "&key=AIzaSyD_QIJehROPYOkn6ww4d7SPtr3jhYETXDo"
    response = requests.get(request_url)
    response_json = response.json()

    city_coordinates = {
        'latitude': response_json['results'][0]['geometry']['location']['lat'],
        'longitude': response_json['results'][0]['geometry']['location']['lng']
    }

    # print(city_coordinates)
    return city_coordinates

def test_get_info_from_weatheronline(cityname):
    
    startday = 1
    # startmonth = 1
    # startyear = 2018

    endday = 30
    # endmonth = 1
    # endyera = ?

    month = 1
    year = 2018
    string = ""
    city_coordinates = get_city_coordinates(cityname)

    city_latitude = city_coordinates['latitude']
    city_longitude = city_coordinates['longitude']

    for day in range(startday, maxday):
        mydate = datetime.date(year, month, day)
        print(mydate)
        print("===")
        unix_date = int(time.mktime(mydate.timetuple()))
        print("new date" + str(unix_date))
        print("___________________")

        request_url = 'https://api.darksky.net/forecast/1161e8117bb9cf0a749d62427a6130ef/'
        request_url = request_url + city_latitude + ',' + city_longitude + ',' + str(unix_date)

        request_url = request_url + '?exclude=currently,flags, minutely, hourly'
        response = requests.get(request_url)

        response_json = response.json()

        monthbydays = response_json['daily']['data'][0]
        string = string + str(monthbydays)
    print("data of month:")
    # print(string)
    # request_url = request_url + cityname
    # request_url = request_url + '&format=json'

    return string
