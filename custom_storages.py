from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """ Create location variable for the S3 static files """
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """ Create location variable for the S3 media files """
    location = settings.MEDIAFILES_LOCATION
