#!/usr/bin/env python3
"""Setups views to handle the ChunkedUpload"""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-24"

# stdlib
import re
from io import BytesIO
from typing import Any, Dict, Tuple

# django
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

# local django
from chunked_upload.constants import COMPLETE, CHUNKED_UPLOAD_CHOICES, http_status
from chunked_upload.exceptions import ChunkedUploadError
from chunked_upload.models import AbstractChunkedUpload, ChunkedUpload
from chunked_upload.views.base_views import ChunkedUploadBaseView
from chunked_upload.response import Response
from chunked_upload.settings import MAX_BYTES
from chunked_upload.views.helpers import is_authenticated

# thirdparty


class ChunkedUploadView(ChunkedUploadBaseView):
    """
    Uploads large files in multiple chunks. Also, has the ability to resume
    if the upload is interrupted.
    """

    field_name = "file"
    user_field_name = "user"
    content_range_header = "HTTP_CONTENT_RANGE"
    content_range_pattern = re.compile(
        r"^bytes (?P<start>\d+)-(?P<end>\d+)/(?P<total>\d+)$"
    )
    max_bytes = MAX_BYTES  # Max amount of data that can be uploaded
    # If `fail_if_no_header` is True, an exception will be raised if the
    # content-range header is not found. Default is False to match Jquery File
    # Upload behavior (doesn't send header if the file is smaller than chunk)
    fail_if_no_header = False

    model = ChunkedUpload

    def get_extra_attrs(self, request: HttpRequest) -> Dict[str, Any]:
        """
        Extra attribute values to be passed to the new ChunkedUpload instance.
        Should return a dictionary-like object.
        """
        attrs = {}
        if (
            hasattr(self.model, self.user_field_name)
            and hasattr(request, "user")
            and is_authenticated(request.user)
        ):
            attrs[self.user_field_name] = request.user
        return attrs

    def get_max_bytes(self, request):
        """
        Used to limit the max amount of data that can be uploaded. `None` means
        no limit.
        You can override this to have a custom `max_bytes`, e.g. based on
        logged user.
        """

        return self.max_bytes

    def get_response_data(self, chunked_upload, request):
        """
        Data for the response. Should return a dictionary-like object.
        """
        return {
            "upload_id": chunked_upload.upload_id,
            "offset": chunked_upload.offset,
            "expires": chunked_upload.expires_on,
        }

    def _post(self, request: HttpRequest, *args, **kwargs):
        try:
            # Execute validation
            self.validate(request)

            chunked_upload = self._put_chunk(request)

            self._save(chunked_upload)

            chunked_upload.complete_upload()

            self.complete_upload(chunked_upload)

            return Response(
                self.get_response_data(chunked_upload, request),
                status=http_status.HTTP_200_OK,
            )
        except ValidationError as err:
            return Response(err, status=http_status.HTTP_400_BAD_REQUEST)

    def _put(self, request, upload_id=None, *args, **kwargs):
        try:
            self.validate(request)

            chunked_upload = self._put_chunk(request)

            self._save(chunked_upload)

            return Response(
                self.get_response_data(chunked_upload=chunked_upload, request=request),
                status=http_status.HTTP_200_OK,
            )
        except ValidationError as err:
            return Response(err, status=http_status.HTTP_400_BAD_REQUEST)
