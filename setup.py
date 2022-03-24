#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("VERSION.txt", "r") as v:
    version = v.read().strip()

with open("README.rst", "r") as r:
    readme = r.read()

download_url = "https://github.com/Vader19695/django-chunky-upload/tarball/%s"

setup(
    name="django-chunky-upload",
    packages=[
        "chunked_upload",
        "chunked_upload.migrations",
        "chunked_upload.management",
    ],
    version=version,
    description=(
        "Upload large files to Django in multiple chunks, with the "
        "ability to resume if the upload is interrupted."
    ),
    long_description=readme,
    author="Jaryd Rester",
    author_email="pypi@jarydrester.com",
    url="https://github.com/Vader19695/django-chunky-upload",
    download_url=download_url % version,
    install_requires=[],
    license="MIT-Zero",
)
