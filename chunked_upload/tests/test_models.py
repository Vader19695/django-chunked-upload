#!/usr/bin/env python3
"""Setups a test for Django"""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-23"

# stdlib

# django
from django.test import TestCase

# local django
from chunked_upload.tests.testapp.models import (
    TEST_CHUNKED_UPLOAD_MODEL,
    TestChunkedUploadModel,
)

# thirdparty
from model_bakery import baker


class ChunkedUploadModelTests(TestCase):
    def test__creating_chunked_upload_works_as_expected(self):
        # assign
        model_instance = baker.make(TEST_CHUNKED_UPLOAD_MODEL)

        # act
        model_instance_qs = TestChunkedUploadModel.objects.get(pk=model_instance.pk)

        # assert
        self.assertIsNotNone(model_instance_qs)
