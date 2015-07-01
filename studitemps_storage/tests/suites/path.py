# coding: utf-8

import unittest
import os

from django.conf import settings

from studitemps_storage.path import guarded_join
from studitemps_storage.path import guarded_safe_join
from studitemps_storage.path import guarded_join_or_create

from studitemps_storage.path import FileSystemNotAvailable

ABSPATH = os.path.abspath(".")
TEST_DIR = os.path.join("studitemps_storage", "tests", "test_dir")

"""
Using unittest.TestCase because we don't need django-Database or Server
"""

class GuardedJoinTestCase(unittest.TestCase):
    def test_file_exists(self):
        """
        it should act like os.path.join
        """

        self.assertEqual(
            guarded_join(ABSPATH, 'studitemps_storage'),
            os.path.join(ABSPATH, 'studitemps_storage')
        )

        self.assertEqual(
            guarded_join(ABSPATH, TEST_DIR, 'check.txt'),
            os.path.join(ABSPATH, TEST_DIR, 'check.txt')
        )

    def test_file_not_exists(self):
        """
        It should raise IOError for not existing file/folder
        """

        self.assertRaises(IOError, guarded_join, ABSPATH, 'files-does-not-exists')

    def test_file_system_not_available(self):
        """
        Manually activates GUARDED_JOIN_TEST to raise FileSystemNotAvailable
        """

        settings.GUARDED_JOIN_TEST = True
        self.assertRaises(FileSystemNotAvailable, guarded_join, ABSPATH)
        settings.GUARDED_JOIN_TEST = False


class GuardedSafeJoin(unittest.TestCase):
    def test_file_exists(self):
        """
        It should act like os.path join with base-folder
        """
        self.assertEqual(
            guarded_safe_join(TEST_DIR, 'check.txt'),
            os.path.join(ABSPATH, TEST_DIR, 'check.txt')
        )

    def test_outside_project(self):
        """
        It should raise exception if try to access files outside project
        """

        self.assertRaises(ValueError, guarded_safe_join, "..", "..", "..")

    def test_not_exists(self):
        """
        It should act like os.path join
        If file/folder doesn't exists returns joined-path
        """

        self.assertEqual(
            guarded_safe_join(TEST_DIR, "file-does-not-exists"),
            os.path.join(ABSPATH, TEST_DIR, "file-does-not-exists")
        )


class GuardedJoinOrCreate(unittest.TestCase):
    def test_file_exists(self):
        """
        It should return path and not create new folder
        """

        self.assertEqual(
            guarded_join_or_create(ABSPATH, 'README.md'),
            os.path.join(ABSPATH, 'README.md')
        )

    def test_create_dir(self):
        """
        Dir does not exists - create new
        """

        path = os.path.join(TEST_DIR, "new-dir")

        # The folder shouldn't exists
        self.assertFalse(os.path.exists(path))

        # The folder should be created
        guarded_join_or_create(path)

        # The folder should be created successful
        self.assertTrue(os.path.exists(path))

        # Remove
        os.rmdir(path)
        self.assertFalse(os.path.exists(path))
