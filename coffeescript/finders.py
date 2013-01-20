from coffeescript.storage import CoffeescriptFileStorage
from django.contrib.staticfiles.finders import BaseStorageFinder


class CoffeescriptFinder(BaseStorageFinder):
    """
    A staticfiles finder that looks in COFFEESCRIPT_ROOT
    for compiled files, to be used during development
    with staticfiles development file server or during
    deployment.
    """
    storage = CoffeescriptFileStorage

    def list(self, ignore_patterns):
        return []
