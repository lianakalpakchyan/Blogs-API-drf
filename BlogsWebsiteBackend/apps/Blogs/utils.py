from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger('main')


def get_path_upload(instance, file):
    logger.info('Creating a path for the image!')
    return f'blog/{instance}/{file}'


def validate_size_image(file_obj):
    megabyte_limit = 2
    logger.info('Checking validation for the image!')
    if file_obj.size > megabyte_limit * 1024 * 1024:
        logger.debug(f'Uploaded an image with a size bigger than {megabyte_limit}MB')
        raise ValidationError(f'Maximum size of the image should be {megabyte_limit}MB')
