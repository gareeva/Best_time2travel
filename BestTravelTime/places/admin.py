from django.contrib import admin

# Register your models here.
from .models import Country
from .models import Indicators_byMonth
from .models import Indicators_byDay
from .models import City

admin.site.register(Country)
admin.site.register(Indicators_byMonth)
admin.site.register(Indicators_byDay)
admin.site.register(City)