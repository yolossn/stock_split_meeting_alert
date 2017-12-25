import requests
from lxml import etree
from datetime import datetime,date
import sys
class stockAlert():
    def __init__(self,url):
        self.url=url
        self.html=""
        self.doc=""
        self.contents=""
        self.event=[]
        self.eventQtly=[]
        self.weekNotify=[]
        self.monthNotify=[]
        self.split=[]
        self.today=date.today()
        self.splitToday=[]
        self.tmrNotify=[]
    def collect(self):
        self.html=requests.get(self.url)
        self.contents=self.html.content
        if self.html.status_code!=200:
            print(self.url,"returned a error while requesting content")
            sys.exit()
        self.doc=etree.HTML(self.contents)
    def scrapEvents(self,):
        companies=self.doc.xpath("//td[1]/a/b/text()")
        link=self.doc.xpath("//td[1]/a/@href")
        dates=self.doc.xpath("//td[2]/text()")
        agendas=self.doc.xpath("//td[3]/text()")
        dates=(datetime.strptime(str(x),"%d-%b-%Y").date() for x in dates)
        for company,href,date,agenda in zip(companies,link,dates,agendas):
            self.event.append({"comp":company,"href":href,"date":date,"agenda":agenda})
        self.eventQtly=[x for x in self.event if x["agenda"]=="Quarterly Results"]
        return self.eventQtly
    def getTmrQtly(self):
        self.tmrNotify=[x for x in self.eventQtly if (x["date"]-self.today).days==1]
        return self.tmrNotify
    def getWeekQtly(self):
        self.weekNotify=[x for x in self.eventQtly if (x["date"]-self.today).days<7]
        return self.weekNotify
    def getMonthQtly(self):
        self.monthNotify=[x for x in self.eventQtly if (x["date"]-self.today).days<30]
        return self.monthNotify
    def scrapSplit(self):
        company=self.doc.xpath("//td[1]/a/b/text()")
        oldfv=self.doc.xpath("//td[2]/text()")
        newfv=self.doc.xpath("//td[3]/text()")
        links=self.doc.xpath("//td[1]/a/@href")
        dates=self.doc.xpath("//td[4]/text()")
        dates=(datetime.strptime(str(x),"%d-%m-%Y").date() for x in dates)
        for comp,date,link,old,new in zip(company,dates,links,oldfv,newfv):
            if (date-self.today).days<0:
                continue
            elif(date-self.today).days==0:
                self.splitToday.append({"comp":comp,"date":date,"href":link,"oldRate":old,"newRate":new})
            self.split.append({"comp":comp,"date":date,"href":link,"oldRate":old,"newRate":new})
        return self.splitToday,self.split
    def __repr__(self):
        string=[]
        for i in range(0,len(self.event)):
            string.append("{}||{}||{}".format(self.event[i]["comp"],self.event[i]["date"],self.event[i]["agenda"]))
        return "\n".join(string)


