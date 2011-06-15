from django.conf.global_settings import *
import os


MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
INSTALLED_APPS = (
    "coffeescript",
)