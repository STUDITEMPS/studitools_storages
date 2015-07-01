import os
import sys

# Sets up django-like-environment because this is not a django project

# Get the project root directory, and add it to `sys.path`.
current_file = __file__
if __name__ == '__main__':
    current_file = '%s/%s' % (os.getcwd(), __file__)
sys.path.insert(0, os.path.realpath(os.path.dirname(current_file) + '/../../'))

# Add the Django settings module to the environment.
os.environ['DJANGO_SETTINGS_MODULE'] = 'studitemps_storage.tests.settings'

# If we're in Django 1.7, we must explicitly set up the
# application registry.
import django
if hasattr(django, 'setup'):
    django.setup()

# Run tests.
from django.core.management import call_command

if __name__ == '__main__':
    args = sys.argv[1:]
    call_command('test', *args)
