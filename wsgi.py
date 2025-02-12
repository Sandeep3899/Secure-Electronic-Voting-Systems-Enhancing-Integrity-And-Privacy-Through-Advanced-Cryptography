"""
WSGI config for e_voting project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

# Importing the os module to interact with the operating system for setting environment variables.
import os

# Importing Django's WSGI application handler, which allows this project to interface with WSGI servers.
from django.core.wsgi import get_wsgi_application

# Setting the default environment variable 'DJANGO_SETTINGS_MODULE' to point to the 'e_voting.settings' module.
# This tells Django to use the settings from the 'settings.py' file within the 'e_voting' project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_voting.settings')

# Creating the WSGI application object that WSGI servers (like Gunicorn or uWSGI) will use to serve the Django project.
application = get_wsgi_application()

