import hashlib  # Importing hashlib to generate hash values (used to generate unique hash IDs).
from os import mkdir  # Importing mkdir to create directories in the file system.

import Pyfhel  # Importing Pyfhel, a library for homomorphic encryption.
from django.contrib import messages  # Importing Django's messages framework to display success/error messages.
from django.contrib.auth import login, logout  # Importing Django's login and logout methods to manage user sessions.
from django.shortcuts import redirect, render, reverse  # Importing redirect, render, and reverse for view logic.

from voting.forms import VoterForm  # Importing VoterForm to handle voter form data.

from .email_backend import EmailBackend  # Importing a custom backend to handle email authentication.
from .forms import CustomUserForm  # Importing a form to handle custom user data.
from Pyfhel import Pyfhel  # Importing the Pyfhel class for homomorphic encryption.
import numpy as np  # Importing numpy for handling numeric operations related to encryption.


# View for handling login.
def account_login(request):
    if request.user.is_authenticated:
        # If the user is already authenticated, redirect them based on their user type.
        if request.user.user_type == "1":
            return redirect(reverse("adminDashboard"))  # Redirect to admin dashboard if the user is an admin.
        else:
            return redirect(reverse("voterDashboard"))  # Redirect to voter dashboard if the user is a voter.

    context = {}  # Initialize an empty context dictionary.
    if request.method == "POST":
        # If the request method is POST, attempt to authenticate the user using the email backend.
        user = EmailBackend.authenticate(
            request,
            username=request.POST.get("email"),
            password=request.POST.get("password"),
        )
        if user != None:  # If the user is successfully authenticated:
            login(request, user)  # Log the user in.
            # Redirect based on user type.
            if user.user_type == "1":
                return redirect(reverse("adminDashboard"))  # Redirect to admin dashboard.
            else:
                return redirect(reverse("voterDashboard"))  # Redirect to voter dashboard.
        else:
            messages.error(request, "Invalid details")  # Display an error message if authentication fails.
            return redirect("/")  # Redirect to the homepage on failure.

    return render(request, "voting/login.html", context)  # Render the login page with the context.


# View for handling user registration.
def account_register(request):
    userForm = CustomUserForm(request.POST or None)  # Instantiate the CustomUser form.
    voterForm = VoterForm(request.POST or None)  # Instantiate the Voter form.
    context = {"form1": userForm, "form2": voterForm}  # Prepare the context with both forms.
    
    if request.method == "POST":
        # If the request method is POST (form submission).
        if userForm.is_valid() and voterForm.is_valid():  # Check if both forms are valid.
            user = userForm.save(commit=False)  # Save the user form without committing to the database yet.
            voter = voterForm.save(commit=False)  # Save the voter form without committing.
            
            # Generate a unique hash ID for the voter based on personal data.
            v = user.last_name + user.first_name + user.email + voter.phone
            hash_id = hashlib.shake_256(v.encode("utf-8")).hexdigest(5)
            voter.hash_id = hash_id  # Assign the hash ID to the voter.
            mkdir(hash_id)  # Create a directory for the voter based on their hash ID.

            # Initialize Pyfhel for encryption.
            fhel = Pyfhel()

            # Generate encryption context and keys.
            fhel.contextGen(scheme="bfv", n=2**14, t_bits=20)  # Set up encryption context.
            fhel.keyGen()  # Generate encryption keys.

            # Encrypt the voter's SSN (convert to integer and remove hyphens).
            int_ssn = int(voter.ssn.replace("-", ""))  # Convert SSN to integer.
            voter.encode_ssn = fhel.encrypt(np.array([int_ssn])).to_bytes()  # Encrypt SSN and store it.
            voter.ssn = "0"  # Reset SSN to 0 for security.

            # Save the encryption keys and context to the voter's directory.
            fhel.save_context(hash_id + "/context")
            fhel.save_public_key(hash_id + "/pub.key")
            fhel.save_secret_key(hash_id + "/sec.key")

            voter.admin = user  # Link the voter to the user account.
            user.save()  # Save the user to the database.
            voter.save()  # Save the voter to the database.
            messages.success(request, "Account created. You can login now!")  # Show success message.
            return redirect(reverse("account_login"))  # Redirect to the login page after successful registration.
        else:
            messages.error(request, "Provided data failed validation")  # Show error message if form validation fails.
    
    return render(request, "voting/reg.html", context)  # Render the registration page with the context.


# View for handling user logout.
def account_logout(request):
    user = request.user  # Get the current user.
    if user.is_authenticated:  # Check if the user is authenticated.
        logout(request)  # Log the user out.
        messages.success(request, "Thank you for visiting us!")  # Show success message after logout.
    else:
        messages.error(request, "You need to be logged in to perform this action")  # Show error if user is not logged in.

    return redirect(reverse("account_login"))  # Redirect to the login page after logout.

