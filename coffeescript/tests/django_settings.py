from django.conf.global_settings import *
import os

DEBUG = True

STATIC_ROOT = MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'static')

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'staticfiles_dir'),
    ("prefix", os.path.join(os.path.dirname(__file__), 'staticfiles_dir_with_prefix')),
)

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
