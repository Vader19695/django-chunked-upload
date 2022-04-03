#!/usr/bin/env python3
"""Setups abstract models for tracking Chunky uploads."""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-25"

# stdlib
from io import BytesIO
import hashlib
from uuid import uuid4

# django
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils import timezone

# local django
from chunked_upload.settings import UPLOAD_TO, STORAGE, EXPIRATION_DELTA

# thirdparty
from chunked_upload.constants import CHUNKED_UPLOAD_CHOICES, COMPLETE, UPLOADING


class AbstractChunkedUpload(models.Model):
    """
    Base chunked upload model. This model is abstract (doesn't create a table
    in the database).
    Inherit from this model to implement your own.
    """

    upload_id = models.UUIDField(unique=True, editable=False, default=uuid4)
    file = models.FileField(max_length=255, upload_to=UPLOAD_TO, storage=STORAGE)
    filename = models.CharField(max_length=255)
    offset = models.BigIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(
        choices=CHUNKED_UPLOAD_CHOICES, default=UPLOADING
    )
    completed_on = models.DateTimeField(null=True, blank=True)

    @property
    def expires_on(self):
        return self.created_on + EXPIRATION_DELTA

    @property
    def expired(self) -> bool:
        return self.expires_on < timezone.now()

    @property
    def md5(self):
        if getattr(self, "_md5", None) is None:
            md5 = hashlib.md5()
            for chunk in self.file.chunks():
                md5.update(chunk)
            self._md5 = md5.hexdigest()
        return self._md5

    def complete_upload(self):
        self.status = COMPLETE
        self.completed_on = timezone.now()
        self.save(
            update_fields=(
                "completed_on",
                "status",
            )
        )

    def delete(self, delete_file=True, *args, **kwargs):
        if self.file:
            storage, path = self.file.storage, self.file.path
        super(AbstractChunkedUpload, self).delete(*args, **kwargs)
        if self.file and delete_file:
            storage.delete(path)

    def __str__(self):
        return "<%s - upload_id: %s - bytes: %s - status: %s>" % (
            self.filename,
            self.upload_id,
            self.offset,
            self.status,
        )

    def append_chunk(self, chunk: InMemoryUploadedFile, chunk_size=None, save=True):
        self.file.close()
        with open(self.file.path, mode="ab") as file_obj:  # mode = append+binary
            chunk_file = chunk.file
            if isinstance(chunk_file, bytes):
                chunk_binary = chunk_file
            elif isinstance(chunk_file, BytesIO):
                print("here")
                chunk_binary = chunk_file.read()

            file_obj.write(
                chunk_binary
            )  # We can use .read() safely because chunk is already in memory

        if chunk_size is not None:
            self.offset += chunk_size
        elif hasattr(chunk, "size"):
            self.offset += chunk.size
        else:
            self.offset = self.file.size
        self._md5 = None  # Clear cached md5
        if save:
            self.save()
        self.file.close()  # Flush

    def get_uploaded_file(self):
        self.file.close()
        self.file.open(mode="rb")  # mode = read+binary
        return InMemoryUploadedFile(
            file=self.file, name=self.filename, size=self.offset
        )

    class Meta:
        abstract = True