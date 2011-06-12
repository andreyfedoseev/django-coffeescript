from ..cache import get_cache_key, get_hexdigest
from ..settings import COFFEESCRIPT_BIN, COFFEESCRIPT_USE_CACHE, COFFEESCRIPT_CACHE_TIMEOUT
from django.core.cache import cache
from django.template.base import Library, Node
import shlex
import subprocess


register = Library()


class CoffeescriptNode(Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def compile(self, source):
        args = shlex.split("%s -c -s -p" % COFFEESCRIPT_BIN)

        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, errors = p.communicate(source.encode("utf-8"))
        if out:
            return out.decode("utf-8")
        elif errors:
            return errors.decode("utf-8")

        return u""

    def render(self, context):
        output = self.nodelist.render(context)

        if COFFEESCRIPT_USE_CACHE:
            cache_key = get_cache_key(get_hexdigest(output))
            cached = cache.get(cache_key, None)
            if cached is not None:
                return cached
            output = self.compile(output)
            cache.set(cache_key, output, COFFEESCRIPT_CACHE_TIMEOUT)
            return output
        else:
            return self.compile(output)

@register.tag(name="coffeescript")
def do_coffeescript(parser, token):
    nodelist = parser.parse(("endcoffeescript",))
    parser.delete_first_token()
    return CoffeescriptNode(nodelist)
