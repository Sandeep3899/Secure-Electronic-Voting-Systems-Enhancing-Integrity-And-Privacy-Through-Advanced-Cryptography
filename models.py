from django.contrib.auth.models import AbstractUser, UserManager  # Importing Django's abstract user model and custom user manager.
from django.db import models  # Importing Django's model framework for database interactions.
from django.contrib.auth.hashers import make_password  # Importing a utility to securely hash passwords.
from django.db.models.signals import post_save  # Importing signals to perform actions after saving a model.
from django.dispatch import receiver  # Importing signal receiver to handle the signals.

# Custom user manager to override the default behavior of user creation.
class CustomUserManager(UserManager):
    
    # Internal method to create and save a user with email and password.
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)  # Normalize the email by converting it to lowercase.
        user = CustomUser(email=email, **extra_fields)  # Create a new CustomUser instance with the provided data.
        user.password = make_password(password)  # Hash the user's password before saving it.
        user.save(using=self._db)  # Save the user to the database.
        return user  # Return the created user object.

    # Public method to create a regular user.
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)  # Ensure regular users are not staff by default.
        extra_fields.setdefault("is_superuser", False)  # Ensure regular users are not superusers by default.
        return self._create_user(email, password, **extra_fields)  # Call the internal _create_user method to save the user.

    # Public method to create a superuser (admin).
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)  # Set the is_staff flag to True for superusers.
        extra_fields.setdefault("is_superuser", True)  # Set the is_superuser flag to True for superusers.
        extra_fields.setdefault("user_type", 1)  # Set the user_type to 1 (Admin).
        extra_fields.setdefault("last_name", "System")  # Set a default last name for the superuser.
        extra_fields.setdefault("first_name", "Administrator")  # Set a default first name for the superuser.

        # Assertions to ensure the proper flags are set for superusers.
        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        
        # Call the internal _create_user method to save the superuser.
        return self._create_user(email, password, **extra_fields)


# Custom user model that extends Django's AbstractUser.
class CustomUser(AbstractUser):
    # Define user types: 1 for Admin, 2 for Voter.
    USER_TYPE = ((1, "Admin"), (2, "Voter"))

    # Remove the default username field, using email as the identifier instead.
    username = None  # The username field is removed because email is used for login.
    email = models.EmailField(unique=True)  # Email field is unique, serving as the login identifier.
    user_type = models.CharField(default=2, choices=USER_TYPE, max_length=1)  # Field to store the user type, defaulting to Voter.
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-populates with the current timestamp when the user is created.
    updated_at = models.DateTimeField(auto_now=True)  # Updates with the current timestamp whenever the user is saved.
    
    # Specify that the email field should be used for authentication instead of the username.
    USERNAME_FIELD = "email"  # Email will be used as the unique identifier for authentication.
    
    # No additional required fields apart from email and password.
    REQUIRED_FIELDS = []  # No extra fields are required when creating a user.

    # Associate the custom user model with the custom user manager.
    objects = CustomUserManager()  # Set the custom manager as the default manager for the CustomUser model.

    # String representation of the user model, showing the user's full name.
    def __str__(self):
        return self.last_name + " " + self.first_name  # Returns the user's full name for display.

