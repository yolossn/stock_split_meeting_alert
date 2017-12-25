import smtplib
from lxml import etree
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
class Email():
    def __init__(self,email,password,subject,recv):
        self.email=email
        self.subject=subject
        self.password=password
        self.recv=recv
        self.server="smtp.gmail.com"
        self.port=57
        session=smtplib.SMTP(self.server)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login(self.email,self.password)
        self.session=session
        self.text=""
        self.html=""
        self.header=[
                "From:"+self.email,
                "Subject:"+self.subject,
                "To:"+self.email,
                "M"
                ]
    def findRate(self,url):
        data={}
        aurl="http://www.moneycontrol.com/india"+url
        resp=requests.get(aurl)
        doc=etree.HTML(resp.content)
        data["bse"]=doc.xpath("//div[2]/div[1]/div[2]/span/strong/text()")
        data["nse"]=doc.xpath("//div[3]/div[1]/div[2]/span/strong/text()")
        return "bse:{}nse:{}".format(data["bse"],data["nse"])
    def sendSplit(self,split,head):
        self.text="\n---------{}----------".format(head)
        self.text+="\n|company|old|new|date|prev close|"
        self.html+="<p><h1>{}</h1></p>".format(head)
        self.html+="""<style>table,th,td,tr{border:2px solid black}</style>
        <table border=2><tr>
        <th>company</th>
        <td>old</th>
        <td>new</th>
        <td>date</th>
        <td>prev Close</td></th>"""
        for stock in split:
            self.text+="|{:7}|{:5}|{:5}|{:10}|{:10}".format(stock["comp"],stock["oldRate"],stock["newRate"],stock["date"],self.findRate(stock["href"]))
            self.html+="""<tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            </tr>""".format(stock["comp"],stock["oldRate"],stock["newRate"],stock["date"],self.findRate(stock["href"]))
        self.html+="</table>"
        return self.text,self.html
    def sendEvent(self,event,head):
        self.text+="\n------{}--------".format(head)
        self.text+="\n|Company|date|agenda|prev close|"
        self.html+="<p><h1>{}</h1></p>".format(head)
        self.html+="""<style>table,th,td,tr{border:2px solid black}</style>
        <table border=2><tr>
        <th>company</th>
        <th>date</th>
        <th>agenda</th>
        <th>prev Close</th></tr>"""
        for eve in event:
            self.text+="\n|{:10}|{:10}|{:10}|{:10}|".format(eve["comp"],eve["date"],eve["agenda"],self.findRate(eve["href"]))
            self.html+="""<tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            """.format(eve["comp"],eve["date"],eve["agenda"],self.findRate(eve["href"]))
        self.html+="</table>"
        return self.text,self.html
    def sendMail(self):
        #print(self.html)
        message=MIMEMultipart('alternative')
        message["From"]=self.email
        message["To"]="".join(self.recv)
        message["Subject"]=self.subject
        text=MIMEText(self.text,'plain')
        html=MIMEText(self.html,'html')
        message.attach(text)
        message.attach(html)
        if(self.html):
            self.session.sendmail(self.email,self.recv,message.as_string())
    def quit(self):
        self.session.quit()
