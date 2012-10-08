#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from time import localtime, strftime

import datetime
import urllib
import xml.dom.minidom

class GismeteoWeather():
    
    def refresh(self):
        valid_casts = Forecast.objects.filter(tstamp__gt=datetime.datetime.now())
        if len(valid_casts) < 3:
            self.get_weather()
            
    def get_weather(self):
#        print "GET_WEATHER!!!"
        Forecast.objects.all().delete()
        
        lstDicXMLNodes = ()
        lstDicXMLNodes=self.parseXMLDoc(self.getXMLDoc())

    def getXMLDoc(self):
        sURL="http://informer.gismeteo.ru/xml/99455_1.xml"
        u=urllib.urlopen(sURL)
        return u.read()

    def parseXMLDoc(self, xmlDoc):
        lstDicXMLNodes=[]
        dicXMLNodes={}
        xmldoc=xml.dom.minidom.parseString(xmlDoc)
        root=xmldoc.documentElement
        for report in root.childNodes:
            if report.nodeName=='#text':
                continue
            for town in report.childNodes:
                if town.nodeName=='#text': 
                    continue
                for cast in town.childNodes:
                    if cast.nodeName=='#text': 
                        continue
                    self.parseForecast(cast)
                        
    def parseForecast(self, cast):
        attrs = cast.attributes
        
        fc = Forecast()
        fc.tod = attrs.item(6).value
        fc.tstamp = datetime.datetime(int(attrs.item(4).value), int(attrs.item(2).value), int(attrs.item(5).value), int(attrs.item(0).value))

        for el in cast.childNodes:
            if el.nodeName=='#text': 
                continue
            attrs = el.attributes
            
            if el.nodeName == 'PHENOMENA':
                fc.spower = attrs.item(0).value
                fc.cloudiness = attrs.item(1).value
                fc.precipitation = attrs.item(2).value
                fc.rpower = attrs.item(3).value
            elif el.nodeName == "PRESSURE":
                fc.pressure_max = attrs.item(0).value
                fc.pressure_min = attrs.item(1).value
            elif el.nodeName == "TEMPERATURE":
                fc.temperature_max = attrs.item(0).value
                fc.temperature_min = attrs.item(1).value
            elif el.nodeName == "WIND":
                fc.wind_max = attrs.item(0).value
                fc.wind_dir = attrs.item(1).value
                fc.wind_min = attrs.item(2).value
            elif el.nodeName == "RELWET":
                fc.relwet_max = attrs.item(0).value
                fc.relwet_min = attrs.item(1).value
            elif el.nodeName == "HEAT":
                fc.heat_max = attrs.item(0).value
                fc.heat_min = attrs.item(1).value

        fc.save()


class Forecast(models.Model):
    tstamp = models.DateTimeField()
    tod = models.IntegerField(unique=True)
   
    cloudiness = models.IntegerField()
    precipitation = models.IntegerField()
    rpower = models.IntegerField()
    spower = models.IntegerField()
    
    pressure_min = models.IntegerField()
    pressure_max = models.IntegerField()
    
    temperature_min = models.IntegerField()
    temperature_max = models.IntegerField()

    wind_min = models.IntegerField()
    wind_max = models.IntegerField()
    wind_dir = models.IntegerField()
    
    relwet_min = models.IntegerField()
    relwet_max = models.IntegerField()
    
    heat_min = models.IntegerField()
    heat_max = models.IntegerField()

    def __unicode__(self):
        return self.tstamp.strftime("%H:%M at %d-%m-%Y")
        
    @property
    def temperature(self):
        return int(0.5*(self.temperature_max+self.temperature_min))
    
    @property
    def daytime(self):
        strdaytime = u'Ночью'
        if self.tod == 1:
            strdaytime = u'Утром'
        elif self.tod == 2:
            strdaytime = u'Днем'
        elif self.tod == 3:
            strdaytime = u'Вечером'
        return strdaytime
        
    @property
    def phenomena(self):
        clouds = u"Ясно"
        if self.cloudiness == 1:
            clouds = u'Малооблачно'
        elif self.cloudiness == 2:
            clouds = u'Облачно'
        elif self.cloudiness == 3:
            clouds = u'Пасмурно'
    
        prec = ''
        if self.precipitation == 4:
            prec = u', дождь'
        elif self.precipitation == 5:
            prec = u', ливень'
        elif self.precipitation == 6 or self.precipitation == 7:
            prec = u', снег'
        elif self.precipitation == 8:
            prec = u', гроза'
            
        return clouds+prec
        
        
        
