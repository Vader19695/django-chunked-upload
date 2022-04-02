#!/usr/bin/env python3
"""Setups testing urls"""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-23"

# stdlib

# django
from django.urls import path, include

# local django

# thirdparty

urlpatterns = [path("", include("chunked_upload.urls"))]
