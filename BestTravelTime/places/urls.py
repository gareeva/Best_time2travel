from django.conf.urls import url

from . import views

app_name = 'places'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    #url(r'^(?P<city_id>[0-9]+)/placedetails/$', views.placedetails, name = 'placedetails'),
    url(r'^date_top/$', views.get_date_top, name = 'date_top'),
    #url(r'^(?P<datetime>[0-9]+)/placestop/$', views.placestop, name = 'placestop'),
    url(r'^city_top/$', views.get_city_top, name = 'city_top'),
]