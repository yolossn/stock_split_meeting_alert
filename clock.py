from apscheduler.schedulers.blocking import BlockingScheduler
from stock import sendAlertMail
sched=BlockingScheduler()
@sched.scheduled_job('cron',day_of_week='mon-sun',hour=11,minute=15)
def scheduled_job():
    sendAlertMail()

sched.start()
