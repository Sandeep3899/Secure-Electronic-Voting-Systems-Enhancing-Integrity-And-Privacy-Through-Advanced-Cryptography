from django.apps import AppConfig  # Importing AppConfig class from Django's built-in apps module.


# Defining a new app configuration class for the 'account' app.
class AccountConfig(AppConfig):
    # The 'name' attribute specifies the name of the app this configuration applies to.
    name = 'account'  # This name refers to the app folder 'account', allowing Django to recognize it.

