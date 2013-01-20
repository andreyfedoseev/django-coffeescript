Django CoffeeScript
===================

Django CoffeeScript provides template tags to compile CoffeeScript into JavaScript from templates.
It works with both inline code and extenal files.

Installation
************

1. Add ``"coffeescript"`` to ``INSTALLED_APPS`` setting.
2. Make sure that you have ``coffee`` executable installed. See
   `CoffeeScript official site <http://jashkenas.github.com/coffee-script/>`_ for details.
3. Optionally, you can specify the full path to ``coffee`` executable with ``COFFEESCRIPT_EXECUTABLE`` setting.
   By default it's set to ``coffee``.
4. In case you use Django’s staticfiles contrib app you have to add django-coffeescript’s file finder to the ``STATICFILES_FINDERS`` setting, for example :

::

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        # other finders..
        'coffeescript.finders.CoffeescriptFinder',
    )

Example Usage
*************

Inline
------

::

    {% load coffeescript %}

    <script type="text/javascript">
      {% inlinecoffeescript %}
        console.log "Hello, World!"
      {% endinlinecoffeescript %}
    </script>

renders to

::

      <script type="text/javascript">
        (function() {
      console.log("Hello, World!");
    }).call(this);

      </script>

External file
-------------

::

    {% load coffeescript %}

    <script type="text/javascript"
            src="{{ STATIC_URL}}{% coffeescript "path/to/script.coffee" %}">
    </script>

renders to

::

    <script type="text/javascript"
            src="/media/COFFEESCRIPT_CACHE/path/to/script-91ce1f66f583.js">
    </script>

Note that by default compiled files are saved into ``COFFEESCRIPT_CACHE`` folder under your ``STATIC_ROOT`` (or ``MEDIA_ROOT`` if you have no ``STATIC_ROOT`` in your settings).
You can change this folder name with ``COFFEESCRIPT_ROOT`` and ``COFFEESCRIPT_OUTPUT_DIR`` settings.


Settings
********

``COFFEESCRIPT_EXECUTABLE``
    Path to CoffeeScript compiler executable. Default: ``"coffee"``.

``COFFEESCRIPT_ROOT``
    Controls the absolute file path that compiled files will be written to. Default: ``STATIC_ROOT``.

``COFFEESCRIPT_OUTPUT_DIR``
    Controls the directory inside ``COFFEESCRIPT_ROOT`` that compiled files will be written to. Default: ``"COFFEESCRIPT_CACHE"``.

``COFFEESCRIPT_USE_CACHE``
    Whether to use cache for inline scripts. Default: ``True``.

``COFFEESCRIPT_CACHE_TIMEOUT``
    Cache timeout for inline scripts (in seconds). Default: 30 days.

``COFFEESCRIPT_MTIME_DELAY``
    Cache timeout for reading the modification time of external scripts (in seconds). Default: 10 seconds.
