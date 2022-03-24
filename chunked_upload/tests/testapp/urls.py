#!/usr/bin/env python3
"""Setups testing urls"""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-23"

# stdlib

# django
from django.urls import path

from chunked_upload.tests.testapp.views import ChunkedUploadTestView

# local django

# thirdparty

urlpatterns = [
    path("upload/", ChunkedUploadTestView, name="upload"),
    path("upload/<uuid:upload_id>/", ChunkedUploadTestView, name="upload"),
]
