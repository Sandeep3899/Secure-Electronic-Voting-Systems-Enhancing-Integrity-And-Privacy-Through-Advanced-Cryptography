from django.shortcuts import render  # Importing the render function to render HTML templates.
from account.views import account_login  # Importing the account_login view from the account app to handle login functionality.

# Defining the 'index' view function which handles the landing page for authenticated users.
def index(request):
    # Check if the user is not authenticated (i.e., not logged in).
    if not request.user.is_authenticated:
        # If the user is not logged in, redirect them to the account login page.
        return account_login(request)
    
    # Initializing an empty context dictionary, which could be used to pass data to the template.
    context = {}

    # The render function is commented out, but this would render the "voting/login.html" template 
    # using the 'context' dictionary. It's likely used to display the login page or some other page if needed.
    # return render(request, "voting/login.html", context)

