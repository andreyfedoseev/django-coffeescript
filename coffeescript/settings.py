from django.conf import settings
import os


POSIX_COMPATIBLE = True if os.name == 'posix' else False
COFFEESCRIPT_EXECUTABLE = getattr(settings, "COFFEESCRIPT_EXECUTABLE", "coffee")
COFFEESCRIPT_USE_CACHE = getattr(settings, "COFFEESCRIPT_USE_CACHE", True)
COFFEESCRIPT_CACHE_TIMEOUT = getattr(settings, "COFFEESCRIPT_CACHE_TIMEOUT", 60 * 60 * 24 * 30) # 30 days
COFFEESCRIPT_MTIME_DELAY = getattr(settings, "COFFEESCRIPT_MTIME_DELAY", 10) # 10 seconds
COFFEESCRIPT_ROOT = getattr(settings, "COFFEESCRIPT_ROOT", getattr(settings, "STATIC_ROOT", getattr(settings, "MEDIA_ROOT")))
COFFEESCRIPT_OUTPUT_DIR = getattr(settings, "COFFEESCRIPT_OUTPUT_DIR", "COFFEESCRIPT_CACHE")
