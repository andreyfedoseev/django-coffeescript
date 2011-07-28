from django.conf.global_settings import *
import os


MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
INSTALLED_APPS = (
    "coffeescript",
)
COFFEESCRIPT_MTIME_DELAY = 2
COFFEESCRIPT_OUTPUT_DIR = "COFFEESCRIPT_CACHE"
