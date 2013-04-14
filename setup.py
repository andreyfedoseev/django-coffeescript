from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


README = read('README.rst')
CHANGES = read('CHANGES.rst')


setup(
    name = "django-coffeescript",
    packages = find_packages(),
    version = "0.7.2",
    author = "Andrey Fedoseev",
    author_email = "andrey.fedoseev@gmail.com",
    url = "https://github.com/andreyfedoseev/django-coffeescript",
    description = "Django template tags to compile CoffeeScript",
    long_description = "\n\n".join([README, CHANGES]),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords = ["coffeescript"],
)
