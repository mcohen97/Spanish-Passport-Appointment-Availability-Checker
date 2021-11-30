# Available slots checker for Spanish Passport

## The problem
Making an appointment to get your Spanish passport in Uruguay is often tedious. The time slots are very scarce, and they become available inadvertedly. They are also taken as soon as they become available.

## The solution
The current project is a bot which checks for avaiable time slots for making appointments to issue the Spanish passport at the Spanish consulate of Uruguay. http://www.exteriores.gob.es/Consulados/MONTEVIDEO/es/Paginas/inicio.aspx.
The bot check every x time for available slots and sends a notification to the specified suscribers. The current notification channels supported are email and whatsapp.
In order to have proper means of monitoring the bot and getting more information about what is happening, the program records logs and saves screenshots every time it checks for availability slots. The logs and screenshots are cleared in intervals of time.

In order to try it:
- Download de project.
- Install the dependencies in requirements.txt
- Specify in a .env file placed in the root folder the following variables:
    - LOGS_DIR: directory for the logs.
    - IMAGES_DIR: directory for the screenshots.
    - WAIT_IN_MINUTES: interval in minutes, which the bot will wait between consecutive checks.
    - LOGS_BACKUP_DAYS: number of days which a log or a screenshot will be kept.
    - EMAIL_SUSCRIBERS: list of comma separated emails of the subscriber who will be notified as soon as availability is found.
    - SENDER_EMAIL: email which will be the sender of the notifications.
    - WHATSAPP_SUSCRIBER_NUMBER: number of one subscriber which will be notified by whatsapp, currently only supporting one single subscriber.
    - CHROMEDRIVER_PATH: path where chromedriver was downloaded.