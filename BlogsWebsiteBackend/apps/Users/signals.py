from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth.models import Permission

from apps.Users.models import User

import logging

logger = logging.getLogger('main')


@receiver(post_save, sender=User)
def status(sender, instance, **kwargs):
    view = Permission.objects.get(name='Can view post')
    add = Permission.objects.get(name='Can add post')
    change = Permission.objects.get(name='Can change post')
    delete = Permission.objects.get(name='Can delete post')
    permissions = [view, add, change, delete]

    if instance.is_superuser:
        instance.role = 'ADMIN'

    if instance.role in ['MODERATOR', 'ADMIN']:
        instance.is_staff = True

        if instance.role == 'ADMIN':
            instance.is_superuser = True

        logger.info('Adding post permissions to a user with a role ADMIN or MODERATOR!')
        for permission in permissions:
            instance.user_permissions.add(permission)
    else:
        instance.is_staff = False
        logger.info('Removing post permissions for a user with a role NON_ADMIN!')
        for permission in permissions:
            instance.user_permissions.remove(permission)

    signals.post_save.disconnect(status, sender=User)
    logger.info('Creating or updating a user!')
    instance.save()
    signals.post_save.connect(status, sender=User)
