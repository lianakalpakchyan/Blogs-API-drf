from django.utils import timezone

from django.db import models
from django.core.validators import FileExtensionValidator

from apps.Users.models import User
from apps.Blogs.utils import get_path_upload, validate_size_image
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
