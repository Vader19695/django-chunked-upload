#!/usr/bin/env python3
"""Setups a signal receiver"""

__author__ = "Jaryd Rester"
__copyright__ = "2022-04-08"

# stdlib

# django
from django.dispatch import receiver

# local django
from chunky_upload.models import ChunkedUpload
from chunky_upload.signals import chunky_upload_complete

# thirdparty


@receiver(
    chunky_upload_complete,
    sender=ChunkedUpload,
    dispatch_uid="handling_upload_complete",
)
def my_callback(sender, **kwargs):
    with open("/tmp/test.txt", "a") as file:
        file.write("Request finished!")
