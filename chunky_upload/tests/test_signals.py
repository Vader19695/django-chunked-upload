#!/usr/bin/env python3
"""Setups a test for Django signals"""

__author__ = "Jaryd Rester"
__copyright__ = "2022-04-08"

# stdlib
from unittest.mock import MagicMock

# django
from django.test import TestCase
from django.utils import timezone

# local django
from chunky_upload.signals import chunky_upload_complete

# thirdparty


class ChunkyUploadCompleteTestCase(TestCase):
    def test__setting_up_signal_receiver_works_as_expected(self):
        # assign
        handler = MagicMock()
        chunky_upload_complete.connect(handler)

        chunky_upload_complete.send(
            sender="test", upload_id="123-456", completed_on=timezone.now
        )

        # assert
        handler.assert_called_once()
