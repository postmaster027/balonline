#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
import datetime
import locale

from cbrexchange.models import CBRExchange
from weather.models import GismeteoWeather, Forecast
from ymapscatalog.models import YandexTraffic, Traffic, Firm

def index(request):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    GismeteoWeather().refresh()
    YandexTraffic().refresh()

    return render_to_response('ymapscatalog/catalog.html',
        {
            'datetime': datetime.datetime.now().strftime('%H:%M, %A, %b %Y'),
            'adrparam': u'Некрасова',
            'firms': Firm.objects.all(),
            'quote': CBRExchange().refresh(),
            'forecasts': Forecast.objects.all().order_by('tstamp'),
            'traffic': Traffic.objects.latest('tstamp')
        },
        context_instance=RequestContext(request))

def detail(request, firm_id):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    firm = get_object_or_404(Firm, pk=firm_id)

    return render_to_response('ymapscatalog/detail.html',
        {
            'datetime': datetime.datetime.now().strftime('%H:%M, %A, %b %Y'),
            'firm': firm
        },
        context_instance=RequestContext(request))

def tagged(request, tag):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    GismeteoWeather().refresh()
    YandexTraffic().refresh()

    return render_to_response('ymapscatalog/catalog.html',
        {
            'datetime': datetime.datetime.now().strftime('%H:%M, %A, %b %Y'),
            'firms': Firm.objects.filter(tags__name=tag),
            'tag': tag,
            'quote': CBRExchange().refresh(),
            'forecasts': Forecast.objects.all().order_by('tstamp'),
            'traffic': Traffic.objects.latest('tstamp')
        },
        context_instance=RequestContext(request))

def traffic(request):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    GismeteoWeather().refresh()
    YandexTraffic().refresh()

    return render_to_response('ymapscatalog/traffic.html',
        {
            'datetime': datetime.datetime.now().strftime('%H:%M, %A, %b %Y'),
            'quote': CBRExchange().refresh(),
            'forecasts': Forecast.objects.all().order_by('tstamp'),
            'traffic': Traffic.objects.latest('tstamp')
        },
        context_instance=RequestContext(request))
