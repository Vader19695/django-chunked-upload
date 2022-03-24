#!/usr/bin/env python3
"""Setups settings for the test Django"""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-23"

# stdlib

# django

# local django

# thirdparty

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "mem_db"}}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "chunked_upload.tests.testapp.apps.TestAppConfig",
    "chunked_upload",
]

CHUNKED_UPLOAD_EXPIRATION_DELTA = 3000
SECRET_KEY = "testing"
