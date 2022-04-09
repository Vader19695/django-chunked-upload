#!/usr/bin/env python3
"""Setups an app for testing the pluggable app."""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-23"

# stdlib

# django
from django.apps import AppConfig

# local django
from chunky_upload.signals import chunky_upload_complete

# thirdparty


class TestAppConfig(AppConfig):
    name = "chunky_upload.tests.testapp"
    verbose_name = "TestApp"

    def ready(self):
        from . import receivers

        chunky_upload_complete.connect(receivers.my_callback)
