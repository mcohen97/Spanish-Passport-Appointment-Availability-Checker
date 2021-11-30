from datetime import datetime, timedelta
import pywhatkit
import logging
import os

from notification_channels.notification_channel import NotificationChannel

class WhatsappNotifier(NotificationChannel):

    def __init__(self, subscribers):
        self.subscribers = subscribers

    def notify_all_suscribers(self, check_result):
        now = datetime.now() + timedelta(minutes=1)
        print(now.hour, now.minute)
        try:
            pywhatkit.sendwhatmsg(os.environ["WHATSAPP_SUSCRIBER_NUMBER"], f"Se ha encontrado horarios disponibles en la fecha {check_result.available_day}", time_hour=now.hour, time_min=now.minute, tab_close=True, wait_time=20)
        except Exception as e:
            logging.error(f"Could not send whatsapp {e}")