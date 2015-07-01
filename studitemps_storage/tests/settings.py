# coding: utf-8

import os

DIRNAME = os.path.dirname(__file__)
DEBUG = True
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(DIRNAME, 'database.db')
SECRET_KEY = 'NOT-EMPTY'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',

    'studitemps_storage',
    'studitemps_storage.tests',
)
GUARDED_JOIN_TEST = False
