from apscheduler.schedulers.background import BackgroundScheduler
from CSharpConWallet.views import user_task


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(user_task, "interval", minutes=60, replace_existing=True)
    scheduler.start()
