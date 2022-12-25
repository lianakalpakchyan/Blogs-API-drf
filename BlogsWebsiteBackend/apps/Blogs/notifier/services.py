import requests
import logging

logger = logging.getLogger('main')


class NotifierService:
    @staticmethod
    def send_email_or_message(instance):
        data = {}
        if instance.status == 'APPROVED':
            data = {
                "event_type": "approved_publication",
                "body": f'Your post "{instance}" is approved',
                "to": instance.author.email
            }
        elif instance.status == 'DENIED':
            data = {
                "event_type": "approved_publication",
                "body": f'Your post "{instance}" is denied',
                "to": instance.author.email
            }
        elif instance.id:
            data = {
                "event_type": "new_publication",
                "body": f'Dear moderator/s there is a new post or update.\nTitle: {instance}\nId: {instance.id}'
            }

        if data:
            try:
                url = 'http://127.0.0.1:5000/events/'
                response = requests.post(url, json=data)
                logger.info(response)
                logger.info(f"Detailed info: {response.text}")
            except Exception as e:
                logger.error(e)
