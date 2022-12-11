from django.utils import timezone

from django.db import models
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import requests

from Users.models import User
from Blogs.base.services import get_path_upload, validate_size_image
import logging

logger = logging.getLogger('main')

ALLOWED_EXTENSIONS = ['jpg', 'jpeg']
UPLOAD_TO = get_path_upload
VALIDATORS = [
    FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS),
    validate_size_image
]


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['id']

    def __str__(self):
        return self.name


class HashTag(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='hash_tag', blank=True)
    name = models.CharField(max_length=140)

    class Meta:
        verbose_name_plural = 'hash-tags'
        ordering = ['id']

    def __str__(self):
        return self.name


class PostImage(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='image', blank=True)
    name = models.ImageField(upload_to=UPLOAD_TO, validators=VALIDATORS)

    class Meta:
        verbose_name_plural = 'images'
        ordering = ['id']

    def __str__(self):
        return f'{self.post}'


class Post(models.Model):
    class Status(models.TextChoices):
        NULL = 'NULL', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        DENIED = 'DENIED', 'Denied'

    title = models.CharField(max_length=100)
    category = models.ManyToManyField('Category', blank=True)
    context = models.TextField(blank=True, default='')
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, default=1)
    status = models.CharField(max_length=80, choices=Status.choices, default=Status.NULL)
    request_date = models.DateTimeField(editable=False)
    publication_date = models.DateTimeField(editable=False, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['request_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.request_date = timezone.now()
        return super(Post, self).save(*args, **kwargs)


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


@receiver(pre_save, sender=Post)
def check_status_for_existing(sender, instance, **kwargs):
    if Post.objects.filter(id=instance.id):
        if instance.status != Post.objects.get(id=instance.id).status:
            if instance.status == 'APPROVED':
                instance.publication_date = timezone.now()
            send_email_or_message(instance)
            logger.info('User is informed regarding his/her post!')
        else:
            instance.request_date = timezone.now()
            instance.publication_date = None
            instance.status = 'NULL'
    else:
        send_email_or_message(instance)


@receiver(post_save, sender=Post)
def check_status_for_new(sender, instance, **kwargs):
    if instance.status == 'NULL':
        logger.info('A post added or updated!')
        send_email_or_message(instance)
        logger.info('Moderators are informed regarding a new post or an update!')
