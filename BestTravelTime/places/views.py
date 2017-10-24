from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.template import loader

from .models import City, Indicators

# Create your views here.
def index(request):
    return HttpResponse("Hey there. You r in main page!")

def placeenterform(request):
    return HttpResponse("enter here the city to visit!")

def timeenterform(request):
    return HttpResponse("enter here the holiday time!")

def placedetails(request, city_id):
    #place_detaled_info = Indicators.objects.get
    return HttpResponse("You are searching for %s" + city_id + " city info")

#require the number of the month for a datetime!
def placestop(request, datetime):
    places_top = []
    places_top = get_indicator_by_month()

    #change when you fix datetime in db!!!
    #places_top = Indicators.objects.filter(datetime = '2017-10-16 18:24:04.000000')

    new_city_list = []
    new_city_list = get_city_info(places_top)
    context = {
        'places_top' : new_city_list,
    }
    return render(request, 'places/index.html', context)

def get_indicator_by_month():
    places_top = []

    all_indicators = Indicators.objects.all()

    for indicator in all_indicators:
        print(indicator)
        #ind.month = str(ind.month)
        #change when you fix datetime in db!!!
        if (str(indicator.month) == '2017-10-16 00:00:00+00:00'):
            places_top.append(indicator)
    return places_top

def get_city_info(places_top):
    new_city_list = []
    for ind in places_top:
        if (City.objects.get(id = ind.city_id)):
            city = City.objects.get(id = ind.city_id)
            new_city_list.append(city)
    return new_city_list
