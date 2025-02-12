from django.utils.deprecation import MiddlewareMixin  # Importing MiddlewareMixin to create a custom middleware class.
from django.urls import reverse  # Importing reverse to resolve view names into URL paths.
from django.shortcuts import redirect  # Importing redirect to send users to different pages.
from django.contrib import messages  # Importing messages to display feedback messages to the user.


# Custom middleware class to check user permissions and redirect accordingly.
class AccountCheckMiddleWare(MiddlewareMixin):
    # Method to process the view request before the view is executed.
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__  # Get the module name of the view being accessed.
        user = request.user  # Get the current logged-in user.

        # Check if the user is authenticated.
        if user.is_authenticated:
            # If the user is an admin (user_type == '1').
            if user.user_type == '1':
                # If the request is for a view in the 'voting.views' module.
                if modulename == 'voting.views':
                    error = True
                    # If the user is trying to fetch a ballot, allow it.
                    if request.path == reverse('fetch_ballot'):
                        pass
                    else:
                        # Otherwise, display an error message and redirect to the admin dashboard.
                        messages.error(request, "You do not have access to this resource")
                        return redirect(reverse('adminDashboard'))

            # If the user is a voter (user_type == '2').
            elif user.user_type == '2':
                # If the user is trying to access an admin page (module 'administrator.views').
                if modulename == 'administrator.views':
                    # Display an error message and redirect to the voter dashboard.
                    messages.error(request, "You do not have access to this resource")
                    return redirect(reverse('voterDashboard'))

            # If the user type is neither admin nor voter, redirect to the login page.
            else:
                return redirect(reverse('account_login'))

        # If the user is not authenticated.
        else:
            # Allow access to the login, registration, and Django authentication views.
            if request.path == reverse('account_login') or request.path == reverse('account_register') or modulename == 'django.contrib.auth.views':
                pass
            # If the user is trying to access an admin or voter page while not logged in.
            elif modulename == 'administrator.views' or modulename == 'voting.views':
                # Display an error message and redirect to the login page.
                messages.error(request, "You need to be logged in to perform this operation")
                return redirect(reverse('account_login'))
            else:
                # Redirect to the login page for any other requests.
                return redirect(reverse('account_login'))

