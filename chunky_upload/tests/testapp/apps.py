#!/usr/bin/env python3
"""Setups an app for testing the pluggable app."""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-23"

# stdlib

# django
from django.apps import AppConfig

# local django

# thirdparty


class TestAppConfig(AppConfig):
    name = "chunky_upload.tests.testapp"
    verbose_name = "TestApp"
