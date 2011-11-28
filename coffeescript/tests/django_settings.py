from django.conf.global_settings import *
import os


STATIC_ROOT = MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
INSTALLED_APPS = (
    "coffeescript",
)
COFFEESCRIPT_MTIME_DELAY = 2
COFFEESCRIPT_OUTPUT_DIR = "COFFEESCRIPT_CACHE"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'coffeescript': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}
