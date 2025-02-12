from django.apps import AppConfig  # Importing AppConfig class from Django's built-in apps module.

# Defining a new app configuration class for the 'voting' app.
class VotingConfig(AppConfig):
    # The 'name' attribute defines the name of the app this configuration applies to.
    name = 'voting'
    # The name 'voting' tells Django this configuration belongs to the 'voting' app.

