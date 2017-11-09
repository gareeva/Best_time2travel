from django.conf.urls import url

from . import views

app_name = 'places'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    #url(r'^(?P<city_id>[0-9]+)/placedetails/$', views.placedetails, name = 'placedetails'),
    url(r'^placedetails/$', views.placedetails, name = 'placedetails'),
    #url(r'^(?P<datetime>[0-9]+)/placestop/$', views.placestop, name = 'placestop'),
    url(r'^placestop/$', views.placestop, name = 'placestop'),
]