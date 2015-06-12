import os

from django.core.files.storage import FileSystemStorage
from django.core.exceptions import SuspiciousOperation

from .path import guarded_join, guarded_safe_join

class GuardedFileSystemStorage(FileSystemStorage):
    """
    like djangos FileSystemStorage, but uses guarded_join to ensure that
    used FileSystem is not hanging.
    """

    def path(self, name):
        try:
            path = guarded_safe_join(self.location, name)
        except ValueError:
            raise SuspiciousOperation("Attempted access to '%s' denied." % name)
        return os.path.normpath(path)
