from rest_framework import serializers
from django.core.files.base import ContentFile
import requests
import base64
import six
import uuid
import logging

logger = logging.getLogger('main')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        logger.info('Image is being processed!')
        if data != 'None':
            data = base64.b64encode(requests.get(data).content).decode('ascii')
            logger.info('Image url address is transformed to base64!')
            if isinstance(data, six.string_types):
                if 'data:' in data and ';base64,' in data:
                    header, data = data.split(';base64,')

                try:
                    decoded_file = base64.b64decode(data)
                except TypeError:
                    logger.error('Invalid image')
                    self.fail('invalid_image')

                file_name = str(uuid.uuid4())[:12]
                file_extension = self.get_file_extension(file_name, decoded_file)

                complete_file_name = "%s.%s" % (file_name, file_extension,)

                data = ContentFile(decoded_file, name=complete_file_name)

            return super(Base64ImageField, self).to_internal_value(data)

        return data

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension
