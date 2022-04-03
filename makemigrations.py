#!/usr/bin/env python3
"""Setups a command to generate migrations"""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-24"

# stdlib
from distutils.command.install import INSTALL_SCHEMES
from distutils.debug import DEBUG
import os

# django
import django
from django.conf import settings
from django.core.management import call_command

# local django

# thirdparty

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "chunky_upload"))


def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "memlocal"}
        },
        INSTALLED_APPS=(
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "chunky_upload",
        ),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()


boot_django()
call_command("makemigrations", "chunky_upload")
