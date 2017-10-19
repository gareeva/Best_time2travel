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
    print(places_top)
    all_indicators = Indicators.objects.all()
    print(all_indicators)
    for ind in all_indicators:
        print(ind)
        #ind.month = str(ind.month)
        if (str(ind.month) == '2017-10-16 00:00:00+00:00'):
            print("success")
            places_top.append(ind)

    #change when you fix datetime in db!!!
    #places_top = Indicators.objects.filter(datetime = '2017-10-16 18:24:04.000000')

    #places_top = Indicators.objects.filter(datetime = '2017-10-16 00:00:00')

    #all_filtered_cities = City.objects.all()
    new_city_list = []
    for ind in places_top:
        print(ind)
        if (City.objects.get(id = ind.city_id)):
            print("city_successsss!!!!")
            city = City.objects.get(id = ind.city_id)
            new_city_list.append(city)
            print(city.city_name + " " + str(city.city_country))

    print(new_city_list[0].city_name + " - " + str(new_city_list[0].city_country))
    template = loader.get_template('places/index.html')
    context = {
        'places_top' : new_city_list,
    }
    #places_top = City.objects.all()
    return HttpResponse(template.render(context, request))