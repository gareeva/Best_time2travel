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
    #change when you fix datetime in db!!!
    places_top = Indicators.objects.filter(datetime = '2017-10-16')
    template = loader.get_template('places/index.html')
    context = {
        'places_top' : places_top,
    }
    #places_top = City.objects.all()
    return HttpResponse(template.render(context, request))