# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formataddr

import os
import logging

from notification_channels.notification_channel import NotificationChannel

class EmailNotifier(NotificationChannel):

    def __init__(self, subscribers, sender_email):
        self.subscribers = subscribers
        self.sender_email = sender_email

    def notify_all_suscribers(self, check_result):
        try:
            msg = MIMEMultipart()
            msg['Subject'] = 'Pasaporte español - Horarios disponibles!!'
            msg['From'] = formataddr(('Horarios de pasaportes (Marcel)', 'diegomarcel1997@gmail.com'))
            msg['To'] = self.subscribers[0]
            body = MIMEText(f"Se ha encontrado horarios disponibles en la fecha {check_result.available_day}")
            msg.attach(body)
            with open(check_result.image_path, 'rb') as f:
                img_data = f.read()
            image = MIMEImage(img_data, name=os.path.basename(check_result.image_path))
            msg.attach(image)

            # Send the message via our own SMTP server, but don't include the
            # envelope header.
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login("diegomarcel1997@gmail.com", "qlrszgbmmjuwisjd")
            server.sendmail("Marcel Cohen", self.subscribers, msg.as_string())
            server.close()
        except Exception as e:
            logging.error(f"Could not send email {e}")