from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
import datetime
import locale

from cbrexchange.models import CBRExchange, Quote
from weather.models import GismeteoWeather, Forecast
from traffic.models import YandexTraffic, Traffic

def index(request):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    
    GismeteoWeather().refresh()
    YandexTraffic().refresh()

    return render_to_response('ymaps/traffic.html', 
    {
    'datetime': datetime.datetime.now().strftime('%H:%M, %A, %b %Y'),
    'quote': CBRExchange().refresh(),
    'forecasts': Forecast.objects.all().order_by('tstamp'),
    'traffic': Traffic.objects.latest('tstamp')
    }, 
    context_instance=RequestContext(request))
