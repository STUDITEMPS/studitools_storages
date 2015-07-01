import os
from subprocess32 import check_call, CalledProcessError, TimeoutExpired

from django.conf import settings
from django.utils._os import safe_join as safe_join

DEFAULT_TIMEOUT = getattr(settings, 'GUARDED_JOIN_TIMEOUT', 1)

def guarded_join(*sub_paths, **kwargs):
    """
    Uses os.path.join to get path from given args.
    checks if path directory is available by using check_call method of
    backport from subprocess module from python 3.X (subprocess32) with given
    timeout and returns path.

    parameters:
        [sub_dirs] (strings) - arguments for os.path.join
        timeout (int) - Timeout for availablity check in sec. (default 1)

    returns:
        path (string)

    possible Exeptions:
        IOError
        FileSystemNotAvailable
    """

    timeout = kwargs.get('timeout', DEFAULT_TIMEOUT)
    full_path = os.path.join(*sub_paths)

    # Move this check here to allow check in runtime
    if getattr(settings, 'GUARDED_JOIN_TEST', False):
        raise FileSystemNotAvailable(
            'This is a test Exception. disable in settings'
        )
    try:
        check_call(['test', '-e', full_path], timeout=timeout)
    except CalledProcessError:
        raise IOError('No such file or directory: %s' % full_path)
    except TimeoutExpired:
        raise FileSystemNotAvailable(
            'Cannot access %s. Tried for %s seconds' % (full_path, timeout)
        )
    return full_path


def guarded_safe_join(base, *paths):
    """
    Uses django safe_join
    https://github.com/django/django/blob/1.6/django/utils/_os.py#L54

    Quote from django:
    Joins one or more path components to the base path component intelligently.
    Returns a normalized, absolute version of the final path.

    The final path must be located inside of the base path component (otherwise
    a ValueError is raised).

    """

    path = safe_join(base, *paths)
    try:
        guarded_join(os.path.dirname(path))
    except IOError:
        pass
    return path


def guarded_join_or_create(*sub_paths, **kwargs):
    """
    Like guarded_join() but never raises IOError. Creates dir
    instead.
    """

    timeout = kwargs.get('timeout', DEFAULT_TIMEOUT)
    try:
        full_path = guarded_join(timeout=timeout, *sub_paths)
    except IOError:
        full_path = os.path.join(*sub_paths)
        os.mkdir(full_path)
    return full_path


class FileSystemNotAvailable(Exception):
    pass
