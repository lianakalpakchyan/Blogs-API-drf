from apps.Blogs.notifier.services import NotifierService


class NotifierProvider:
    @staticmethod
    def send_email_or_message(instance):
        service = NotifierService()
        return service.send_email_or_message(instance)
