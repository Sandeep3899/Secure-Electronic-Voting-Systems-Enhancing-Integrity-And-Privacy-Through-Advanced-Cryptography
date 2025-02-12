from django.contrib.auth.backends import ModelBackend  # Importing Django's default model backend for authentication.
from django.contrib.auth import get_user_model  # Importing the method to get the active user model in the project.


# Custom authentication backend that uses email instead of username for authentication.
class EmailBackend(ModelBackend):
    
    # The 'authenticate' method is overridden to provide custom authentication logic.
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()  # Get the active user model in the project (usually 'CustomUser' in this case).
        
        try:
            # Try to find the user based on the provided email (which is passed as 'username').
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # If no user with the provided email is found, return None (authentication fails).
            return None
        else:
            # If the user is found, check if the provided password matches the user's password.
            if user.check_password(password):  # The 'check_password' method securely compares passwords.
                return user  # If the password matches, return the user object (authentication is successful).
        
        return None  # If the password does not match, return None (authentication fails).

