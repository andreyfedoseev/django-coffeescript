from unittest import main, TestCase
from django.template.base import Template
from django.template.context import RequestContext
import os
import re
import time


os.environ["DJANGO_SETTINGS_MODULE"] = "coffeescript.tests.django_settings"


class CoffeeScriptTestCase(TestCase):

    def setUp(self):
        pass

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
        self.assertEqual(template.render(RequestContext({})).strip(), rendered)

    def test_external_coffeescript(self):
        from coffeescript import settings as coffeescript_settings
        coffeescript_settings.COFFEESCRIPT_MTIME_DELAY = 2

        template = Template("""
        {% load coffeescript %}
        {% coffeescript "scripts/test.coffee" %}
        """)
        compiled_filename_re = re.compile(r"COFFEESCRIPT_CACHE/scripts/test-[a-f0-9]{12}.js")
        compiled_filename = template.render(RequestContext({})).strip()
        self.assertTrue(bool(compiled_filename_re.match(compiled_filename)))

        from django.conf import settings
        compiled_path = os.path.join(settings.MEDIA_ROOT, compiled_filename)
        compiled_content = open(compiled_path).read()
        compiled = """(function() {
  console.log("Hello, World!");
}).call(this);
"""
        self.assertEquals(compiled_content, compiled)

        # Change the modification time
        source_path = os.path.join(settings.MEDIA_ROOT, "scripts/test.coffee")
        os.utime(source_path, None)

        # The modification time is cached so the compiled file is not updated
        compiled_filename_2 = template.render(RequestContext({})).strip()
        self.assertTrue(bool(compiled_filename_re.match(compiled_filename_2)))
        self.assertEquals(compiled_filename, compiled_filename_2)

        # Wait to invalidate the cached modification time
        time.sleep(coffeescript_settings.COFFEESCRIPT_MTIME_DELAY)

        # Now the file is re-compiled
        compiled_filename_3 = template.render(RequestContext({})).strip()
        self.assertTrue(bool(compiled_filename_re.match(compiled_filename_3)))
        self.assertNotEquals(compiled_filename, compiled_filename_3)

        
if __name__ == '__main__':
    main()