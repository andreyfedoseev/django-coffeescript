from unittest import main, TestCase
from django.http import HttpRequest
from django.template.base import Template
from django.template.context import RequestContext
import os
import re
import time
import shutil


os.environ["DJANGO_SETTINGS_MODULE"] = "coffeescript.tests.django_settings"


class CoffeeScriptTestCase(TestCase):

    def setUp(self):
        from django.conf import settings as django_settings
        self.django_settings = django_settings

        output_dir = os.path.join(self.django_settings.STATIC_ROOT,
                                  self.django_settings.COFFEESCRIPT_OUTPUT_DIR)

        # Remove the output directory if it exists to start from scratch
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

    def _get_request_context(self):
        return RequestContext(HttpRequest())

    def _clean_javascript(self, js):
        """ Remove comments and all blank lines. """
        return "\n".join(line for line in js.split("\n") if line.strip() and not line.startswith("//"))

    def test_inline_coffeescript(self):
        template = Template("""
        {% load coffeescript %}
        {% inlinecoffeescript %}
          console.log "Hello, World"
        {% endinlinecoffeescript %}
        """)
        rendered = """(function() {
  console.log("Hello, World");
}).call(this);"""
        self.assertEqual(
            self._clean_javascript(template.render(self._get_request_context()).strip()),
            self._clean_javascript(rendered)
        )

    def test_external_coffeescript(self):

        template = Template("""
        {% load coffeescript %}
        {% coffeescript "scripts/test.coffee" %}
        """)
        compiled_filename_re = re.compile(r"COFFEESCRIPT_CACHE/scripts/test-[a-f0-9]{12}.js")
        compiled_filename = template.render(self._get_request_context()).strip()
        self.assertTrue(bool(compiled_filename_re.match(compiled_filename)))

        compiled_path = os.path.join(self.django_settings.STATIC_ROOT, compiled_filename)
        compiled_content = open(compiled_path).read()
        compiled = """(function() {
  console.log("Hello, World!");
}).call(this);
"""
        self.assertEquals(
            self._clean_javascript(compiled_content),
            self._clean_javascript(compiled)
        )

        # Change the modification time
        source_path = os.path.join(self.django_settings.STATIC_ROOT, "scripts/test.coffee")
        os.utime(source_path, None)

        # The modification time is cached so the compiled file is not updated
        compiled_filename_2 = template.render(self._get_request_context()).strip()
        self.assertTrue(bool(compiled_filename_re.match(compiled_filename_2)))
        self.assertEquals(compiled_filename, compiled_filename_2)

        # Wait to invalidate the cached modification time
        time.sleep(self.django_settings.COFFEESCRIPT_MTIME_DELAY)

        # Now the file is re-compiled
        compiled_filename_3 = template.render(self._get_request_context()).strip()
        self.assertTrue(bool(compiled_filename_re.match(compiled_filename_3)))
        self.assertNotEquals(compiled_filename, compiled_filename_3)

        # Check that we have only one compiled file, old files should be removed

        compiled_file_dir = os.path.dirname(os.path.join(self.django_settings.STATIC_ROOT,
                                                         compiled_filename_3))
        self.assertEquals(len(os.listdir(compiled_file_dir)), 1)

    def test_lookup_in_staticfiles_dirs(self):
        template = Template("""
        {% load coffeescript %}
        {% coffeescript "another_test.coffee" %}
        """)
        compiled_filename_re = re.compile(r"COFFEESCRIPT_CACHE/another_test-[a-f0-9]{12}.js")
        compiled_filename = template.render(self._get_request_context()).strip()
        self.assertTrue(bool(compiled_filename_re.match(compiled_filename)))

        compiled_path = os.path.join(self.django_settings.STATIC_ROOT, compiled_filename)
        compiled_content = open(compiled_path).read()
        compiled = """(function() {
  console.log("Hello, World from STATICFILES_DIRS!");
}).call(this);
"""
        self.assertEquals(
            self._clean_javascript(compiled_content),
            self._clean_javascript(compiled)
        )


        template = Template("""
        {% load coffeescript %}
        {% coffeescript "prefix/another_test.coffee" %}
        """)
        compiled_filename_re = re.compile(r"COFFEESCRIPT_CACHE/prefix/another_test-[a-f0-9]{12}.js")
        compiled_filename = template.render(self._get_request_context()).strip()
        self.assertTrue(bool(compiled_filename_re.match(compiled_filename)))

        compiled_path = os.path.join(self.django_settings.STATIC_ROOT, compiled_filename)
        compiled_content = open(compiled_path).read()
        compiled = """(function() {
  console.log("Hello, World from STATICFILES_DIRS with prefix!");
}).call(this);
"""
        self.assertEquals(
            self._clean_javascript(compiled_content),
            self._clean_javascript(compiled)
        )

if __name__ == '__main__':
    main()
