from ..cache import get_cache_key, get_hexdigest, get_hashed_mtime
from django.contrib.staticfiles import finders
from ..settings import COFFEESCRIPT_EXECUTABLE, COFFEESCRIPT_USE_CACHE,\
    COFFEESCRIPT_CACHE_TIMEOUT, COFFEESCRIPT_ROOT, COFFEESCRIPT_OUTPUT_DIR,\
    POSIX_COMPATIBLE
from django.conf import settings
from django.core.cache import cache
from django.template.base import Library, Node, TemplateSyntaxError
import logging
import shlex
import subprocess
import os


STATIC_ROOT = getattr(settings, "STATIC_ROOT", getattr(settings, "MEDIA_ROOT"))


logger = logging.getLogger("coffeescript")


register = Library()


class InlineCoffeescriptNode(Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def compile(self, source):
        args = shlex.split(
            "%s -c -s -p" % COFFEESCRIPT_EXECUTABLE, posix=POSIX_COMPATIBLE
        )

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


@register.tag(name="inlinecoffeescript")
def do_inlinecoffeescript(parser, token):
    nodelist = parser.parse(("endinlinecoffeescript",))
    parser.delete_first_token()
    return InlineCoffeescriptNode(nodelist)


def coffeescript_paths(path):

    full_path = os.path.join(STATIC_ROOT, path)

    if settings.DEBUG and not os.path.exists(full_path):
        # while developing it is more confortable
        # searching for the coffeescript files rather then
        # doing collectstatics all the time
        full_path = finders.find(path)

        if full_path is None:
            raise TemplateSyntaxError("Can't find staticfile named: {}".format(path))

    file_name = os.path.split(path)[-1]
    output_dir = os.path.join(COFFEESCRIPT_ROOT, COFFEESCRIPT_OUTPUT_DIR, os.path.dirname(path))

    return full_path, file_name, output_dir


@register.simple_tag
def coffeescript(path):
    logger.info("processing file %s" % path)

    full_path, file_name, output_dir = coffeescript_paths(path)

    hashed_mtime = get_hashed_mtime(full_path)

    base_file_name = file_name.replace(".coffee","")

    output_file = "%s-%s.js" % (base_file_name, hashed_mtime)
    output_path = os.path.join(output_dir, output_file)

    if not os.path.exists(output_path):
        source_file = open(full_path)
        source = source_file.read()
        source_file.close()

        args = shlex.split(
            "%s -c -s -p" % COFFEESCRIPT_EXECUTABLE,
             posix=POSIX_COMPATIBLE
        )
        p = subprocess.Popen(args, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, errors = p.communicate(source)

        if errors:
            logger.error(errors)
            return path

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        compiled_file = open(output_path, "w+")
        compiled_file.write(out)
        compiled_file.close()

        # Remove old files
        compiled_filename = os.path.split(output_path)[-1]
        for filename in os.listdir(output_dir):
            if filename.startswith(base_file_name) and filename != compiled_filename:
                os.remove(os.path.join(output_dir, filename))

    return os.path.join(COFFEESCRIPT_OUTPUT_DIR, os.path.dirname(path), output_file)
