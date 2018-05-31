from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.template import loader

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
import requests
import json
import time, datetime, calendar

from .models import City, Indicators_byMonth, Country, Indicators_byDay



# Create your views here.
def index(request):
    return render(request, 'places/index.html')

def placeenterform(request):
    return HttpResponse("enter here the city to visit!")

def timeenterform(request):
    return HttpResponse("enter here the holiday time!")

#def placedetails(request, city_id):
def get_date_top(request):
    entered_city= request.POST.get('cityname', False);
    
    if (entered_city != "test"):
        city = City.objects.get(city_name = entered_city)
        # переписать эту часть! пересмотреть логику!
        place_info = []
        place_indicators = Indicators_byMonth.objects.all()
        for indicator in place_indicators:
            print(indicator)
            if (indicator.city == city):
                place_info.append(indicator)

        context = {
            'place_name' : str(entered_city),
            'place_info' : place_info,
            'error_message' : "No such a city! Please enter another one!",
        }
        # must be entered from form in future
        # !!!!!!!!!!! uncomment this part after testing
        # startdate = datetime.date(2018, 3, 1)
        # enddate = datetime.date(2018, 4, 1)
        # data = check_month_date_existence(city, startdate, enddate)

        data = test_data_generator(city)

        return HttpResponse(data)
    else:
        data = test_data_generator()
        return HttpResponse(data)
    
    #chanfge the variables when cleaned
    #return render(request, 'places/city_details.html', context)

    #change to id later! Because you will need to automate the entering


#require the number of the month for a datetime!
def get_city_top(request):
    entered_start_datetime = request.POST.get('startdate', False)
    entered_end_datetime = request.POST.get('enddate', False)

    city_list = City.objects.all()

    for city in city_list:
        check_month_date_existence(city, entered_start_datetime, entered_end_datetime)

    calculate_month_score()
    make_city_rating()

    #change when you fix datetime in db!!!
    places_top = Indicators_byMonth.objects.filter(datetime = '2018-10-16 18:24:04.000000')

    new_city_list = []
    new_city_list = get_city_list(places_top)
    context = {
        'places_top' : new_city_list,
    }

    return HttpResponse(data)

    #return render(request, 'places/index.html', context)
    # return render(request, 'places/places_top.html', context)

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


def get_city_coordinates(city):
    request_url =  "https://maps.googleapis.com/maps/api/geocode/json?address="
    request_url = request_url + city.city_name + "&key=AIzaSyD_QIJehROPYOkn6ww4d7SPtr3jhYETXDo"
    response = requests.get(request_url)
    response_json = response.json()

    city_coordinates = {
        'latitude': response_json['results'][0]['geometry']['location']['lat'],
        'longitude': response_json['results'][0]['geometry']['location']['lng']
    }
    return city_coordinates



def create_Indicators_byDay(file_row, city, mydate):
    daily_record = Indicators_byDay(
        city= city, 
        date = mydate)

    if 'icon' in file_row:
        daily_record.icon = file_row['icon']
    if 'apparentTemperatureHigh' in file_row:
        daily_record.apparent_temp_high = file_row['apparentTemperatureHigh']
    if 'apparentTemperatureLow' in file_row:
        daily_record.apparent_temp_low = file_row['apparentTemperatureLow']
    if 'apparentTemperatureMin' in file_row:
        daily_record.apparent_temp_min = file_row['apparentTemperatureMin']
    if 'apparentTemperatureMax' in file_row:
        daily_record.apparent_temp_max = file_row['apparentTemperatureMax']
    if 'temperatureMin' in file_row:
        daily_record.temp_min = file_row['temperatureMin']
    if 'temperatureMax' in file_row:
        daily_record.temp_max = file_row['temperatureMax']


    if 'humidity' in file_row:
        daily_record.humidity = file_row['humidity']
    if 'moonPhase' in file_row:
        daily_record.moonphase = file_row['moonPhase']
    
    if 'precipIntensityMax' in file_row:
        daily_record.precip_intencity_max = file_row['precipIntensityMax']
    elif 'precipIntensity' in file_row:
        daily_record.precip_intencity_max = file_row['precipIntensity']
    
    if 'precipAccumulation' in file_row:
        daily_record.precip_accumulation_max = file_row['precipAccumulation']
    
    if 'precipType' in file_row:
        daily_record.precip_type = file_row['precipType']
    if 'windSpeed' in file_row:
        daily_record.wind_speed = file_row['windSpeed']
    if 'visibility' in file_row:
        daily_record.visibility = file_row['visibility']
    if 'pressure' in file_row:
        daily_record.pressure = file_row['pressure']
        
    daily_record.save(force_insert=True)

def calculate_fields_byMonth(year, month, city):
    monthly_record = Indicators_byMonth(
        city= city, 
        month = month)

    month_last_day = calendar.monthrange(year, month)[1]
    D1 = datetime.date.toordinal(datetime.date(year, month, 1))
    D2 = datetime.date.toordinal(datetime.date(year, month, month_last_day))

    # D1 = datetime.date.toordinal(datetime.date(2018, month, 1))
    # D2 = datetime.date.toordinal(datetime.date(2018, month + 1, 1))

    count_temp = count_humidity = count_precip_intencity = count_precip_accum = count_wind = count_visibility = count_pressure = 0
    
    # !выяснить, какое значение подставляется, если сразу плюсовать в переменную

    average_apparent_temp = average_humidity = wet_days_count = average_precipitation_intencity = average_precipitation_accumulation = average_wind_speed = average_visibility = pressure = count_of_rain_days = count_of_snow_days = count_of_sleet_days =  count_of_cloudy_days = count_of_clear_days = count_of_wind_days = count_of_fog_days = 0
    
    for some_day in range(D1,D2+1):
        date = datetime.date.fromordinal(some_day)
        daily_record = Indicators_byDay.objects.get(city = city, date = date)

        # print("--date in month:", date, daily_record)
        
        if (daily_record.precip_intencity_max is not None):
            if (daily_record.precip_intencity_max > 0.1 and daily_record.precip_intencity_max < 7.6):
                wet_days_count += 1
        if (daily_record.apparent_temp_high is not None or daily_record.apparent_temp_low is not None):
            average_apparent_temp += (daily_record.apparent_temp_high + daily_record.apparent_temp_low) / 2
            count_temp += 1
        if (daily_record.humidity is not None):
            average_humidity += daily_record.humidity 
            count_humidity += 1
        if (daily_record.precip_intencity_max is not None):
            average_precipitation_intencity += daily_record.precip_intencity_max 
            count_precip_intencity += 1
        if (daily_record.precip_accumulation_max is not None):
            average_precipitation_accumulation += daily_record.precip_accumulation_max 
            count_precip_accum += 1
        if(daily_record.wind_speed is not None):
            average_wind_speed += daily_record.wind_speed
            count_wind += 1
        if (daily_record.visibility is not None):
            average_visibility += daily_record.visibility
            count_visibility += 1
        if (daily_record.pressure is not None):
            pressure += daily_record.pressure
            count_pressure += 1

        # TBD!
        if (daily_record.precip_type is not None):
            if (daily_record.precip_type == 'rain'):
                count_of_rain_days += 1
            if (daily_record.precip_type == 'snow'):
                count_of_snow_days += 1
        if (daily_record.icon is not None):
            # if daily_record.icon == 'rain':
            if daily_record.icon == 'sleet':
                count_of_sleet_days += 1
            if daily_record.icon in ['cloudy', 'partly-cloudy-night', 'partly-cloudy-day']:
                count_of_cloudy_days += 1
            if (daily_record.icon == 'clear-day' or daily_record.icon == 'clear-night'):
                count_of_clear_days += 1
            if daily_record.icon == 'wind':
                count_of_wind_days += 1
            if daily_record.icon == 'fog':
                count_of_fog_days += 1

# # setting into object fields 
    if(count_temp != 0): monthly_record.average_apparent_temp = average_apparent_temp/count_temp
    else: monthly_record.average_apparent_temp = 0
    
    if(count_humidity != 0): monthly_record.average_humidity = average_humidity/count_humidity
    else: monthly_record.average_humidity = 0
    
    if(count_visibility != 0): monthly_record.average_visibility = average_visibility/count_visibility
    else: monthly_record.average_visibility = 0

    if(count_wind != 0): monthly_record.average_wind_speed = average_wind_speed/count_wind
    else: monthly_record.wind_speed = 0

    if(count_precip_intencity != 0): monthly_record.average_precipitation_intencity = average_precipitation_intencity/count_precip_intencity
    else: monthly_record.average_precipitation_intencity = 0

    if(count_precip_accum != 0): monthly_record.average_precipitation_accumulation = average_precipitation_accumulation/count_precip_accum
    else: monthly_record.average_precipitation_accumulation = 0

    if(count_pressure != 0): monthly_record.pressure = pressure/count_pressure
    else: monthly_record.pressure = 0

    monthly_record.wet_days_count = wet_days_count
    monthly_record.count_of_rain_days = count_of_rain_days
    monthly_record.count_of_snow_days = count_of_snow_days
    monthly_record.count_of_sleet_days = count_of_sleet_days
    monthly_record.count_of_cloudy_days = count_of_cloudy_days
    monthly_record.count_of_clear_days = count_of_clear_days
    monthly_record.count_of_wind_days = count_of_wind_days
    monthly_record.count_of_fog_days = count_of_fog_days

    print(str(monthly_record))
    calculate_month_score(monthly_record, count_temp, count_precip_intencity, count_visibility)

    monthly_record.save(force_insert=True)
    return monthly_record

def calculate_month_score(month, count_temp, count_precip_intencity, count_visibility):
    total_score = 0
    total_score += calculate_precipitation_score(month,count_precip_intencity)
    total_score += calculate_visibility_score(month,count_visibility)
    total_score += calculate_temperature_score(month, count_temp)

    print("total_score = ",total_score)
    month.month_score = total_score

def calculate_precipitation_score(month, count_precip_intencity):
    if (count_precip_intencity != 0):
        precipitation = month.average_precipitation_intencity
        print("precipitation = " + str(precipitation) + " count_precip_intencity=" + str(count_precip_intencity) )
        if (precipitation >= 0 and precipitation <= 2.5):
            return 1
        elif (precipitation > 2.5 and precipitation <= 7.6):
            return 6
        elif(precipitation > 7.6):
            return 12
    else:
        rainy_days = month.count_of_rain_days
        print("rainy_days = " + str(rainy_days))
        if (rainy_days <= 5):
            return 1
        elif(rainy_days > 5 and rainy_days <= 10):
            return 6
        elif(rainy_days > 10):
            return 12


def calculate_visibility_score(month, count_visibility):
    if (count_visibility != 0):
        visibility = month.average_visibility
        print("visbility = " + str(visibility))
        if (visibility >= 1):
            return 1
        elif (visibility > 0.5 and visibility < 1):
            return 6
        elif (visibility < 0.5 and visibility != 0):
            return 12
        else:
            return 0
    else:
        snowy_days = month.average_visibility
        print("snowy_days = " + str(snowy_days))
        if (snowy_days <= 5):
            return 1
        elif(snowy_days > 5 and snowy_days <= 10):
            return 6
        elif(snowy_days > 10):
            return 12

def calculate_temperature_score(month, count_temp):
    if(count_temp != 0):
        temperature = month.average_apparent_temp
        print("temp = "+ str(temperature))
        if (temperature < -32):
            return 12
        elif (temperature > -32 and temperature <= -24):
            return 11
        elif (temperature > -24 and temperature <= -10):
            return 9
        elif (temperature > -10 and temperature <= 0):
            return 8
        elif (temperature > 0 and temperature <= 7):
            return 7
        elif (temperature > 7 and temperature <= 11):
            return 6
        elif (temperature > 11 and temperature <= 15):
            return 5
        elif (temperature > 15 and temperature <= 20):
            return 4
        elif (temperature > 20 and temperature <= 24):
            return 2
        elif (temperature > 24 and temperature <= 28):
            return 1
        elif (temperature > 28 and temperature <= 33):
            return 3
        elif (temperature > 33):
            return 10
    else:
        print("temperature is not defined!!!!!!!!")

def check_month_date_existence(city, startdate, enddate):
    D1 = datetime.date.toordinal(startdate)
    D2 = datetime.date.toordinal(enddate)

    while D1 <= D2:
        current_date = datetime.date.fromordinal(D1)
        current_date_extracted = datetime.datetime.strptime(str(current_date), "%Y-%m-%d")
        current_date_month = current_date_extracted.month
        current_date_year = current_date_extracted.year
        current_date_month_days_count = calendar.monthrange(current_date_extracted.year, current_date_month)[1]

        if (Indicators_byMonth.objects.filter(city=city, month = current_date_month).exists()):
            print("data for this month already exists = ", current_date_month)
            answer = Indicators_byMonth.objects.filter(city=city, month = current_date_month)
            break
        else:
            print("search new data for month = ", current_date_month)
            new_startdate = datetime.date(current_date_year, current_date_month, 1)
            new_enddate = datetime.date(current_date_year, current_date_month, current_date_month_days_count)
            answer = get_info_from_weatheronline(city, new_startdate, new_enddate)
            calculate_fields_byMonth(current_date_year, current_date_month, city)
        D1 += current_date_month_days_count
    return answer

def get_info_from_weatheronline(city, startdate, enddate):
    output_to_me = ""
    # DATE1 = datetime.date(startdate)
    # DATE2 = datetime.date(enddate)
    D1 = datetime.date.toordinal(startdate)
    D2 = datetime.date.toordinal(enddate)

    for some_day in range(D1,D2+1):
        date = datetime.date.fromordinal(some_day)
        # print (date)
        if (check_data_existence(city, date)):
            output_to_me += str(Indicators_byDay.objects.get(city = city, date = date))
        else:
            # print("Accessing new day from API")
            unix_date = int(time.mktime(date.timetuple()))
            city_coordinates = get_city_coordinates(city)
            city_latitude = str(city_coordinates['latitude'])
            city_longitude = str(city_coordinates['longitude'])
            response = request_to_weatheronline(city_latitude, city_longitude, unix_date)
            output_to_me += str(response_parsing(response, city, date))
    return output_to_me


def check_data_existence(city, date):
    # required_city = City.objects.get(city_name = city)
    if (Indicators_byDay.objects.filter(city=city, date = date).exists()):
        print("data already exists for day = " + str(date))
        return True
    return False

def request_to_weatheronline(city_latitude, city_longitude, unix_date):
    request_url = 'https://api.darksky.net/forecast/1161e8117bb9cf0a749d62427a6130ef/'
    request_url = request_url + city_latitude + ',' + city_longitude + ',' + str(unix_date)
    request_url = request_url + '?exclude=currently,flags,minutely,hourly&units=si'
    # print("===================")
    # print(request_url)
    response = requests.get(request_url)
    return response

def response_parsing(response, city, mydate):
    response_json = response.json()
    daily_data = response_json['daily']['data'][0]
    create_Indicators_byDay(daily_data, city, mydate)
    return daily_data

def test_data_generator(city):
    year = 2018

    for month in range(1, 13):
        print("month = " + str(month))
        # city = City.objects.get(city_name = 'kazan')

        last_day = calendar.monthrange(year, month)[1]
        startdate = datetime.date(year, month, 1)
        enddate = datetime.date(year, month, last_day)
        print("startdate = " + str(startdate) + "; enddate = " + str(enddate))

        # if (month != 12):
        #     startdate = datetime.date(2018, month, 1)
        #     enddate = datetime.date(2018, month+1, 1)
        #     print("startdate = " + str(startdate) + "; enddate = " + str(enddate))
        # else:
        #     startdate = datetime.date(2018, month, 1)
        #     enddate = datetime.date(2018, month, 31)
            
        data = check_month_date_existence(city, startdate, enddate)
    
    make_month_rating(city)
    return data

def make_month_rating(city):
    months_list = Indicators_byMonth.objects.filter(city = city).order_by('month_score', '-average_apparent_temp', '-count_of_clear_days')
    for each in months_list:
        print("rating: " + str(each))

    return months_list


def make_city_rating(month):
    city_list = Indicators_byMonth.objects.filter(month = month).order_by('month_score', '-average_apparent_temp', '-count_of_clear_days')
    for each in city_list:
        print("rating: " + str(each))

    return city_list


