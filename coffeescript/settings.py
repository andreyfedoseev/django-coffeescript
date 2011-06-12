from django.conf import settings


COFFEESCRIPT_BIN = getattr(settings, "COFFEESCRIPT_BIN", "coffee")
COFFEESCRIPT_USE_CACHE = getattr(settings, "COFFEESCRIPT_USE_CACHE", True)
COFFEESCRIPT_CACHE_TIMEOUT = getattr(settings, "COFFEESCRIPT_CACHE_TIMEOUT", 60 * 60 * 24) # 1 day