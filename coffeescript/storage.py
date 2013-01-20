from django.core.files.storage import FileSystemStorage
from coffeescript.settings import COFFEESCRIPT_ROOT


class CoffeescriptFileStorage(FileSystemStorage):
    """
    Standard file system storage for files handled by django-coffeescript.

    The default for ``location`` is ``COFFEESCRIPT_ROOT``
    """
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        if location is None:
            location = COFFEESCRIPT_ROOT
        super(CoffeescriptFileStorage, self).__init__(location, base_url,
                                                *args, **kwargs)
