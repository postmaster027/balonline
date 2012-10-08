from django.db import models
from time import localtime, strftime

import datetime
import urllib
import xml.dom.minidom

class CBRExchange():

    def refresh(self):
        quote = False
        try:
            quote = Quote.objects.get(tstamp=datetime.date.today())
        except:
            quote = self.get_quotes()
            quote.save()
        return quote
        
    def get_quotes(self):
#        print "GET_QUOTES!!!"
        quote = Quote()
        quote.tstamp = datetime.date.today()

        lstDicXMLNodes=self.ekParseXMLDoc(self.ekGetInput())

        for dicXMLNode in lstDicXMLNodes:
            nodeNumCode = int(dicXMLNode['NumCode'])
            nodeValue = float(dicXMLNode['Value'].replace(",","."))
            if nodeNumCode == 840:
                quote.usd = nodeValue
            elif nodeNumCode == 978:
                quote.eur = nodeValue
        return quote

    def ekGetInput(self):
        sURL="http://www.cbr.ru/scripts/XML_daily.asp?date_req=%s" % (strftime("%d.%m.%Y", localtime()))
        u=urllib.urlopen(sURL)
        return u.read()

    def ekParseXMLDoc(self, xmlDoc):
        lstDicXMLNodes=[]
        dicXMLNodes={}
        xmldoc=xml.dom.minidom.parseString(xmlDoc)
        root=xmldoc.documentElement
        for valute in root.childNodes:
            if valute.nodeName=='#text':
                continue
#            print valute.nodeName
            for ch in valute.childNodes:
                if ch.nodeName=='#text': # Drop TextNode, that is means "\n" in the xml document
                    continue
#                print ch.nodeName, ch.childNodes[0].nodeValue
                dicXMLNodes[ch.nodeName]=ch.childNodes[0].nodeValue
            lstDicXMLNodes.append(dicXMLNodes)
            dicXMLNodes={}
        return lstDicXMLNodes

class Quote(models.Model):
    tstamp = models.DateField(unique=True)
    usd = models.FloatField(default=0.0)
    eur = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.tstamp.strftime("%d-%m-%Y")

