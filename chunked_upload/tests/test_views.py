#!/usr/bin/env python3
"""Setups testing for views"""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-23"

# stdlib

# django
from django.urls import reverse
from django.test import TestCase, Client

# local django

# thirdparty


class ChunkedUploadTests(TestCase):
    def test__initial_patch_works_as_expected(self):
        # assign
        client = Client()

        # act
        print(reverse("upload"))
        response = client.patch(reverse("upload"))

        # assert
        self.assertEqual(response.status_code, 200)
