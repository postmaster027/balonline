from django.db import models
from time import localtime, strftime

import datetime
import urllib
import xml.dom.minidom

class Quote(models.Model):
    date = models.DateField(unique=True)
    usd = models.FloatField(default=0.0)
    eur = models.FloatField(default=0.0)

    def __unicode__(self):
        return strftime("%d-%m-%Y", localtime())

    def ekGetInput(self, sDate):
        sURL="http://www.cbr.ru/scripts/XML_daily.asp?date_req=%s" % (sDate)
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


    def save(self):
        self.date = datetime.date.today()
        print self.date
        
        sDate = strftime("%d.%m.%Y", localtime())

        lstDicXMLNodes = ()
        lstDicXMLNodes=self.ekParseXMLDoc(self.ekGetInput(sDate))

        for dicXMLNode in lstDicXMLNodes:
            nodeNumCode = int(dicXMLNode['NumCode'])
            nodeValue = float(dicXMLNode['Value'].replace(",","."))
#            print nodeNumCode, nodeValue
            if nodeNumCode == 840:
                self.usd = nodeValue
            elif nodeNumCode == 978:
                self.eur = nodeValue
        try:
            super(Quote, self).save()
        except:
            pass
