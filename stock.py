import scrap
import mail
from credentials import getKeys
from datetime import datetime,date
import sys
#if __name__=="__main__":
def sendAlertMail():
    urlBoard="http://www.moneycontrol.com/stocks/marketinfo/meetings.php?opttopic=brdmeeting"
    urlSplit="http://www.moneycontrol.com/stocks/marketinfo/splits/index.php"
    today=date.today()
    eid,pwd=getKeys()
    """------------
    scrap url split
    ------------"""
    alertSplit=scrap.stockAlert(urlSplit)
    alertSplit.collect()
    m,p=alertSplit.scrapSplit()
    """------------
    scrap meeting
    ------------"""
    alertBoard=scrap.stockAlert(urlBoard)
    alertBoard.collect()
    alertBoard.scrapEvents()
    d=alertBoard.getTmrQtly()
    """------------
    mailing part
    ------------"""
    smail=mail.Email(eid,pwd,"Stock-Alert",["emailID"])
    if(d):
        a,b=smail.sendEvent(d,"Quaterly Meeting Tomorrow")
    if(m):
        a,b=smail.sendSplit(m,"Split Today")
    if today.day==1:
        s=alertBoard.getMonthQtly()
        a,b=smail.sendEvent(s,"Monthly Quaterly Meeting")
        smail.sendMail()
        smail.quit()
        sys.exit()
    if today.weekday()==6:
        if(p):
            a,b=smail.sendSplit(p,"Weekly Split")
        s=alertBoard.getWeekQtly()
        a,b=smail.sendEvent(s,"Weekly Quaterly Meeting")
    smail.sendMail()
    smail.quit()
