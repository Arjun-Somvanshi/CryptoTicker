import schedule
import time
from app.database import db, update_alert, update_user, get_user
from app.ticker import get_bitcoin_price
from app.model import AlertSchema, UserSchema

def update_alert_and_user(targetAlert: dict):
    update_alert(targetAlert, {"$set": {"status": "triggered"}})
    user = db["users"].find_one({"email": targetAlert["email"]})
    for alert in user["alerts"]:
        if alert["alert_id"] == targetAlert["alert_id"]:
            alert["status"] = "triggered"
            break
    update_user(user)
    #logger.info("Alert ID: " + str(targetAlert.alert_id) + " was triggered")

def job(logger):
    logger.info("CryptoTicker Alert Job Running....\n")
    alertCollection  = db["alerts"]
    btc_price = get_bitcoin_price()
    for alert in alertCollection.find({"status": "created"}):
        logger.info(str(btc_price) + " " + str(alert["targetPrice"]))
        if alert["targetPrice"] >= alert["currentPrice"]:
            if alert["targetPrice"]  <= btc_price:
                update_alert_and_user(alert)
                log = alert["alert_id"] + " was triggered :)"
                logger.info(log)
                #send email
        else:
            if alert["targetPrice"]  >= get_bitcoin_price():
                update_alert_and_user(alert)
                log = alert["alert_id"] + " was triggered :)"
                logger.info(log)
                #send email


def execute_job(logger):
    job(logger)
    schedule.every(30).seconds.do(job, logger=logger)
    while True:
        schedule.run_pending()

if __name__ == "__main__":
    execute_job()
