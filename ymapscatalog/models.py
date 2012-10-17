#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from time import localtime, strftime

import datetime, time, string
from datetime import timedelta

import urllib
import json

from taggit.managers import TaggableManager

class Firm(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(blank=True, null=True, upload_to='firms')
    phone = models.CharField(max_length="100")
    url = models.CharField(max_length="80", null=True)
    location = models.CharField(max_length="240", null=True)
    about  = models.TextField(max_length=320, null=True)
    xcord = models.FloatField(default=55.81)
    ycord = models.FloatField(default=37.953)
    rating = models.IntegerField(default=0)
    tags = TaggableManager()




    def __unicode__(self):
        return self.name

    @property
    def contacts(self):
        pass



class YandexTraffic():

    def refresh(self):
        last_valid = datetime.datetime.now()-datetime.timedelta(0, 1800, 0)
        valid = Traffic.objects.filter(tstamp__gt=last_valid).count()
        #        print 'last_:', last_valid, 'exists:', valid

        if valid < 1:
            self.get_traffic()

    def get_traffic(self):
    #        print "GET_TRAFFIC!!!"

        u=urllib.urlopen("http://api-maps.yandex.ru/services/traffic-info/1.0/?format=json&lang=ru-RU")
        jsonDoc = u.read()

        obj = json.loads(jsonDoc)[u'GeoObjectCollection']
        collection = obj[u'features']
        for item in collection:
            if item[u'name'] == u'Москва':
                targ = item[u'properties'][u'JamsMetaData']

                tr = Traffic()
                tr.city_name = item[u'name']
                tr.color = targ[u'icon']
                tr.level = targ[u'level']
                tr.tstamp = datetime.datetime.fromtimestamp(targ[u'timestamp'])
                tr.save()

class Traffic(models.Model):
    tstamp = models.DateTimeField()
    city_name = models.CharField(max_length=80)
    color = models.CharField(max_length=10)
    level = models.IntegerField()

    def __unicode__(self):
        return u'Пробки от '+self.tstamp.strftime("%H:%M at %d-%m-%Y")

#    @property
#    def temperature(self):
#        return int(0.5*(self.temperature_max+self.temperature_min))

