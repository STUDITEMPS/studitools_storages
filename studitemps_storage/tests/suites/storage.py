# coding: utf-8

import unittest
import os

from studitemps_storage.storage import GuardedFileSystemStorage

from django.core.files.base import ContentFile
from django.core.exceptions import SuspiciousOperation

ABSPATH = os.path.abspath(".")
TEST_DIR = os.path.join("studitemps_storage", "tests", "test_dir")

class StorageTest(unittest.TestCase):
    def setUp(self):
        self.storage = GuardedFileSystemStorage()

    def test_read(self):
        """
        File should be accessable and readable from storage
        """

        check_file_name = os.path.join(TEST_DIR, "check.txt")
        self.assertEqual(
            self.storage.exists(check_file_name),
            os.path.exists(check_file_name)
        )

        # Check if the cotents is readable
        check_file = self.storage.open(check_file_name, "rb")
        self.assertEqual(
            check_file.read(),
            "This file is present and should not be deleted"
        )
        check_file.close()

    def test_create_and_delete(self):
        file_content = u"THIS is the new content"

        # Check if new File exists
        new_file_name = os.path.join(TEST_DIR, "new_file.txt")
        self.assertFalse(self.storage.exists(new_file_name))

        # write new File
        self.storage.save(new_file_name, ContentFile(file_content))

        # Reopen and check if content is present
        check_file = self.storage.open(new_file_name, "rb")
        self.assertEqual(check_file.read(), file_content)

        # Delete file
        self.storage.delete(new_file_name)

        # File should be deleted
        self.assertFalse(self.storage.exists(new_file_name))

    def test_access_outside_project(self):
        """
        It should detect access outside projectdir and raise exception
        """
        self.assertRaises(SuspiciousOperation, self.storage.exists, "../../../")

        self.assertRaises(SuspiciousOperation, self.storage.exists, "../../")

        self.assertRaises(SuspiciousOperation, self.storage.exists, "../")

        self.assertTrue(self.storage.exists("."))
