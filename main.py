import time
from datetime import datetime, timedelta
from notification_channels.email_notifier import EmailNotifier
from notification_channels.whatsapp_notifier import WhatsappNotifier
import passport_appointment_checker
import logging
import threading
import os
from dotenv import load_dotenv
load_dotenv()

LOGS_DIR = os.environ['LOGS_DIR']
IMAGES_DIR = os.environ['IMAGES_DIR']
WAIT_IN_MINUTES = int(os.environ['WAIT_IN_MINUTES'])
LOGS_BACKUP_DAYS = int(os.environ['LOGS_BACKUP_DAYS'])

logging.basicConfig(filename=f"{LOGS_DIR}/app_logs.log", 
                    level=logging.INFO, 
                    format='%(asctime)s %(levelname)-8s %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')


email_suscribers = os.environ["EMAIL_SUSCRIBERS"].split(",")
sender_email = os.environ["SENDER_EMAIL"]
notifiers = [
    EmailNotifier(subscribers=email_suscribers, sender_email= os.environ["SENDER_EMAIL"]), 
    WhatsappNotifier(subscribers=[])
    ]

def main():
    images_cleaning = threading.Thread(target=delete_old_images, name="ScreenshotsCleaning")
    images_cleaning.start()

    while True:
        logging.info(f"Checking availability")
        availability_checker = passport_appointment_checker.PassportAppointmentChecker(screenshots_dir=IMAGES_DIR)
        availability_check_result = availability_checker.check_available_slots_for_spanish_passport_issuance()
        if availability_check_result.is_slot_available:
            for notifier in notifiers:
                notifier.notify_all_suscribers(availability_check_result)
        logging.info(f"Wait for {WAIT_IN_MINUTES}")
        time.sleep(WAIT_IN_MINUTES * 60)

def delete_old_images():
    while True:
        criticalTime = datetime.now() - timedelta(days=LOGS_BACKUP_DAYS)

        for item in os.listdir(IMAGES_DIR):
            item = f"./{IMAGES_DIR}/{item}"
            itemTime = os.stat(item).st_mtime
            if itemTime < criticalTime.timestamp():
                os.remove(item)

        open(f"{LOGS_DIR}/app_logs.log", "w").close()

        time.sleep(LOGS_BACKUP_DAYS*3600*24)

main()
