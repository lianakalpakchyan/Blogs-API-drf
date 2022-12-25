from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

import logging
from apps.Blogs.models import Post
from apps.Blogs.notifier.providers import NotifierProvider

logger = logging.getLogger('main')


@receiver(pre_save, sender=Post)
def check_status_for_existing(sender, instance, **kwargs):
    notifier = NotifierProvider()
    if Post.objects.filter(id=instance.id):
        if instance.status != Post.objects.get(id=instance.id).status:
            if instance.status == 'APPROVED':
                instance.publication_date = timezone.now()
            notifier.send_email_or_message(instance)
            logger.info('User is informed regarding his/her post!')
        else:
            instance.request_date = timezone.now()
            instance.publication_date = None
            instance.status = 'NULL'
    else:
        notifier.send_email_or_message(instance)


@receiver(post_save, sender=Post)
def check_status_for_new(sender, instance, **kwargs):
    notifier = NotifierProvider()
    if instance.status == 'NULL':
        logger.info('A post added or updated!')
        notifier.send_email_or_message(instance)
        logger.info('Moderators are informed regarding a new post or an update!')
