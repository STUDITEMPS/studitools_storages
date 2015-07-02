# Studitemps-Tools Storages

studitemps_storage is a package with helper funtions for File IO. It only works
in a Django Context. By now it includes three modules:

- `path`: Contains Basic File IO Functions for general usage
- `storage`: Django File Storage that make use of functions in path.py
- `middleware`: Django Middleware related to the usage of the other packages

# Installation
Install the package via PIP

  git+http://phabricator.intranet.studitemps.de/diffusion/STOR/studitools_storages.git#TAG

# Configuration

## Sets the default storage-engine

  DEFAULT_FILE_STORAGE = 'studitemps_storage.GuardedFileSystemStorage'

## Adds the middleware class

  MIDDLEWARE_CLASSES = (
   ...
   'studitemps_storage.CatchFileSystemNotAvailableMiddleware',
   ...
  )

## Sets the timeout in secs for checking if resource is available

  GUARDED_JOIN_TIMEOUT = 1  # default


## This is used for Unittesting to raise the error

  GUARDED_JOIN_TEST = False  # default
 
## Error-Template
guarded_join raises `FileSystemNotAvailable` and the `CatchFileSystemNotAvailableMiddleware` catches this.
Make sure you have a template-file `504.html`.


# Usage

## guarded_join
Uses os.path.join to get path from given args.
checks if path directory is available by using check_call method of
backport from subprocess module from python 3.X (subprocess32) with given
timeout and returns path.

  from studitemps_storage import guarded_join

## guarded_safe_join
Uses **from django.utils._os import safe_join**
https://github.com/django/django/blob/1.6/django/utils/_os.py#L54

> Joins one or more path components to the base path component intelligently.
> Returns a normalized, absolute version of the final path.
> 
> The final path must be located inside of the base path component (otherwise
> a ValueError is raised).

  from studitemps_storage import guarded_safe_join

## guarded_join_or_create
like guarded_join() but never raises IOError. Creates dir
instead.

  from studitemps_storage import guarded_join_or_create

# Unittests
To run unittests-suites

  python studitemps_storage/tests/runtests.py suites


# Update guide
If you make changes to this repo, please make sure:

* Update TestCases according to code-changes
* All- and your Tests are still running
* Update README.md
  - Docs. with changes
  - Changelog with Changes and the new version
* Update setup.py `version` at line 22
* Commit and create your new Tag


# Changelog

## v0.1.1

* Bumped v0.1.1
* Update Usage-docs
 
## v0.1.0

* Bumped v0.1.0
* Update README.md
* Update docs
* Add unittest for `path` and `storage`
* Fixed guarded_join_or_create AttributeError

## v0.0.2

* Project Init