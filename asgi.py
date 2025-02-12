"""
ASGI config for e_voting project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

# Importing the os module to interact with the operating system environment variables.
import os

# Importing the Django ASGI application handler, which allows this Django project to interface with an ASGI server.
from django.core.asgi import get_asgi_application

# Setting the default settings module for the Django project. This tells Django which settings to use (from e_voting/settings.py).
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_voting.settings')

# Creating an ASGI application instance, which can be used to handle ASGI requests.
application = get_asgi_application()

