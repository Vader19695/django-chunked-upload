#!/usr/bin/env python3
"""Setups testing for views"""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-23"

# stdlib
import hashlib
from ast import literal_eval
from io import BytesIO
from unittest.mock import patch

# django
from django.core.files.base import ContentFile
from django.test import TestCase, Client
from django.urls import reverse


# local django
from chunked_upload.constants import http_status

# thirdparty
from model_bakery import baker


class ChunkedUploadViewTests(TestCase):
    def test__putting_initial_chunk_works_as_expected(self):
        # assign
        client = Client()
        binary_data = BytesIO(b"test file").getvalue()

        # act
        response = client.put(
            reverse("upload-view"),
            {"file": binary_data, "filename": "simplefile.txt"},
            headers={
                "HTTP_CONTENT_RANGE": f"0-{len(binary_data)}/{len(binary_data)}",
                "Content-Disposition": f'attachment; filename="simplefile.txt"',
            },
        )

        # assert
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

    def test__putting_additional_chunk_works_as_expected(self):
        # assign
        client = Client()
        original_binary_data = b"test file"
        binary_data = BytesIO(b" new test file data").getvalue()
        chunked_upload = baker.make(
            "chunked_upload.ChunkedUpload",
            file=ContentFile(original_binary_data, "name"),
        )

        # act
        response = client.put(
            reverse("upload-view", args=(chunked_upload.upload_id,)),
            {"file": binary_data, "filename": "simplefile.txt"},
            headers={
                "HTTP_CONTENT_RANGE": f"{len(original_binary_data)}-{len(binary_data)}/{len(binary_data) + len(original_binary_data)}",
                "Content-Disposition": f'attachment; filename="simplefile.txt"',
            },
        )

        # assert
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        self.assertEqual(
            open(chunked_upload.file.path, "r").read(), "test file new test file data"
        )

    @patch("chunked_upload.views.base_views.ChunkedUploadBaseView.complete_upload")
    def test__posting_verifies_the_upload_and_marks_the_upload_as_complete(
        self, patched_complete_upload
    ):
        # assign
        client = Client()
        original_binary_data = b"test file"
        md5 = hashlib.md5()
        md5.update(original_binary_data)
        checksum = md5.hexdigest()
        chunked_upload = baker.make(
            "chunked_upload.ChunkedUpload",
            file=ContentFile(original_binary_data, "name"),
        )

        # act
        response = client.post(
            reverse("upload-view", args=(chunked_upload.upload_id,)),
            data={
                "md5": checksum,
            },
            content_type="application/json",
        )

        # assert
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        patched_complete_upload.assert_called()

    def test__posting_raises_an_exception_when_md5_is_incorrect(self):
        # assign
        client = Client()
        original_binary_data = b"test file"
        md5 = hashlib.md5()
        md5.update(original_binary_data + b"testing")
        checksum = md5.hexdigest()
        chunked_upload = baker.make(
            "chunked_upload.ChunkedUpload",
            file=ContentFile(original_binary_data, "name"),
        )

        # act
        response = client.post(
            reverse("upload-view", args=(chunked_upload.upload_id,)),
            data={
                "md5": checksum,
            },
            content_type="application/json",
        )

        # assert
        self.assertEqual(response.status_code, http_status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            literal_eval(response.content.decode())["detail"],
            "md5 checksum does not match",
        )
