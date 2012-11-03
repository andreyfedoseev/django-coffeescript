from ..cache import get_cache_key, get_hexdigest, get_hashed_mtime
from ..settings import COFFEESCRIPT_EXECUTABLE, COFFEESCRIPT_USE_CACHE,\
    COFFEESCRIPT_CACHE_TIMEOUT, COFFEESCRIPT_OUTPUT_DIR, POSIX_COMPATIBLE
from django.conf import settings
from django.core.cache import cache
from django.template.base import Library, Node
from os.path import join, dirname, exists, basename
import logging
import shlex
import subprocess
import os


logger = logging.getLogger("coffeescript")
register = Library()


class InlineCoffeescriptNode(Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def compile(self, source):
        args = shlex.split("%s -c -s -p" % COFFEESCRIPT_EXECUTABLE, posix=POSIX_COMPATIBLE)

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

    try:
        root = settings.STATIC_ROOT
    except AttributeError:
        root = settings.MEDIA_ROOT

    # while developing it is more confortable
    # searching for the coffeescripts rather then 
    # doing collectstatics all the time
    if settings.DEBUG:
        for sfdir in settings.STATICFILES_DIRS:
            prefix = None
            if isinstance(sfdir, (tuple, list)):
                prefix, sfdir = sfdir
            if prefix:
                if not path.startswith(prefix):
                    continue
                input_file = join(sfdir, path[len(prefix):].lstrip(os.sep))
            else:
                input_file = join(sfdir, path)
            if exists(input_file):
                output_dir = join(root, COFFEESCRIPT_OUTPUT_DIR, dirname(path))
                file_name = basename(path)
                return input_file, file_name, output_dir
    
    full_path = os.path.join(root, path)
    file_name = os.path.split(path)[-1]
    
    output_dir = os.path.join(root, COFFEESCRIPT_OUTPUT_DIR, os.path.dirname(path))
    
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

        args = shlex.split("%s -c -s -p" % COFFEESCRIPT_EXECUTABLE, posix=POSIX_COMPATIBLE)
        p = subprocess.Popen(args, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, errors = p.communicate(source)
        if out:
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
        elif errors:
            logger.error(errors)
            return path

    return join(COFFEESCRIPT_OUTPUT_DIR, dirname(path), output_file)
