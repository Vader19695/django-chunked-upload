#!/usr/bin/env python3
"""Setups urls for Chunky upload."""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-25"

# stdlib

# django
from django.urls import path

from chunked_upload.views import ChunkedUploadView

# local django

# thirdparty

urlpatterns = [
    path("upload/", ChunkedUploadView.as_view(), name="upload-view"),
    path("upload/<uuid:upload_id>/", ChunkedUploadView.as_view(), name="upload-view"),
]
