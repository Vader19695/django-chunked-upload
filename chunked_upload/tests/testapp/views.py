#!/usr/bin/env python3
"""Setups views for testing"""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-23"

# stdlib

# django

# local django
from chunked_upload.views import ChunkedUploadBaseView

# thirdparty


class ChunkedUploadTestView(ChunkedUploadBaseView):
    pass
