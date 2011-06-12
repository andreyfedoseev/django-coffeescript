from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor
import socket


def get_hexdigest(plaintext, length=None):
    digest = md5_constructor(smart_str(plaintext)).hexdigest()
    if length:
        return digest[:length]
    return digest


def get_cache_key(key):
    return ("django_coffescript.%s.%s" % (socket.gethostname(), key))
