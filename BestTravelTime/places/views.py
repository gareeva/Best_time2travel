from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.template import loader

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import City, Indicators

# Create your views here.
def index(request):
    return render(request, 'places/index.html')
    #return HttpResponse("Hey there. You r in main page!")

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
    place_indicators = Indicators.objects.all()
    for indicator in place_indicators:
        print(indicator)
        #if (3 == 3):
        if (indicator.city_id == required_city.id):
            place_info.append(indicator)

    context = {
        'place_info' : place_info,
    }

    return render(request, 'places/city_details.html', context)
    #change to id later! Because you will need to automate the entering
    

    #return HttpResponse(required_city.city_country)

    
    
    #print(str(required_city.id) + "-" + required_city.city_name + "-"+ str(required_city.city_country_id))
    
    #place_details = []
    #place_details = Indicators.objects.filter(city = required_city.id)
    #or indicator in place_details:
    #    print(str(indicator.city) + "-" + str(indicator.temperature) + "-" + str(indicator.precipitation))
    #context = {
     #   'place_info' : place_details,
    #}
    #return render(request, 'places/city_details.html', context)

#require the number of the month for a datetime!
def placestop(request, datetime):
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
    all_indicators = Indicators.objects.all()

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
