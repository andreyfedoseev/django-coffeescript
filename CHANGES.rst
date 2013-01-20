Changes
*******

0.7
----

- Add COFFEESCRIPT_ROOT setting
- Add staticfiles finder to serve compiled files in dev mode


0.6
----

- Switch to staticfiles.finders when looking up the files in DEBUG mode.


0.5.1
-----

- Add support for STATICFILES_DIRS with prefixes

0.5
----

- When in DEBUG mode lookup coffee scripts in all STATICFILES_DIRS

0.4
----

- Log coffeescript compilation errors
- Fixed bug with paths on Windows (by syabro)

0.3
----

- Use STATIC_ROOT / STATIC_URL settings when possible instead of MEDIA_ROOT / MEDIA_URL (by Roman Vorushin)

0.2.1
-----

- Add CHANGES.rst to MANIFEST.in

0.2
----

- Automatically remove old files from COFFEESCRIPT_CACHE
- Add basic unit tests

0.1
----

- Initial release
