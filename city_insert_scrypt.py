 file = open('/Users/liana/Developer/Best_time2travel/BestTravelTime/res_cities.txt','r')
 for line in file:
        
        splitted_line = []
        splitted_line = line.split('\t')
        cityname = splitted_line[0]

        citycountryshort = splitted_line[2]
        new = []
        new = citycountryshort.split('\n')

        try:
            common_country = Country.objects.get(short_name = new[0])
            new_city = City(city_country = common_country, city_name = cityname)
            # print(new_city.city_name + " " + new_city.city_country)

            print(new_city)
            new_city.save()
        except Country.DoesNotExist:
            print("noooo")

    file.close()