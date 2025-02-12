#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
# This script is the entry point for executing various Django management tasks such as running the development server, 
# migrating the database, or creating a superuser.

import os  # Importing the os module to interact with the operating system.
import sys  # Importing the sys module to handle command-line arguments and system-specific functions.


def main():
    """Run administrative tasks."""
    # This function is the main entry point for executing Django's administrative tasks.

    # Set the default Django settings module for the 'e_voting' project.
    # This ensures that the settings file is used when Django commands are run.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_voting.settings')

    try:
        # Try to import Django's function for executing command-line tasks.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django isn't installed or can't be imported, raise an error with a helpful message.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Run the command-line utility with the provided arguments (from sys.argv).
    # This allows you to run commands like 'runserver', 'migrate', 'createsuperuser', etc.
    execute_from_command_line(sys.argv)


# The script starts execution here.
if __name__ == '__main__':
    # If this file is executed directly (instead of being imported as a module), call the main() function.
    main()

