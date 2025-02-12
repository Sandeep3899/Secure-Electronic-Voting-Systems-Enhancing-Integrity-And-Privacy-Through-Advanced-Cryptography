from django import forms  # Importing Django's forms module to create form classes.
from .models import *  # Importing all models from the current app to use in forms.
from account.forms import FormSettings  # Importing custom form settings from the 'account' app for base settings.
from django.utils import timezone  # Importing Django's timezone utility for handling dates and times.
from datetime import timedelta  # Importing timedelta for date calculations.
import re  # Importing the regular expressions module to validate the SSN format.


# Defining the form for the Voter model, which inherits from custom FormSettings.
class VoterForm(FormSettings):
    class Meta:
        # Specifies the model and fields for this form.
        model = Voter  # This form is based on the Voter model.
        fields = ["phone", "ssn", "dob"]  # The fields that will be displayed and processed in the form.

        # Customizing widgets for the form fields.
        widgets = {
            "ssn": forms.TextInput(
                attrs={
                    "placeholder": "XXX-XX-XXXX",  # Placeholder text guiding the SSN format.
                    "pattern": r"\d{3}-\d{2}-\d{4}",  # HTML5 pattern for basic SSN validation.
                    "maxlength": "11",  # Maximum length for the SSN input.
                    "title": "Enter SSN in the format XXX-XX-XXXX",  # Tooltip text for guidance on SSN input.
                }
            ),
            "dob": forms.DateInput(attrs={"type": "date"}),  # Using HTML5 date input for the date of birth.
        }

        # Customizing the labels for the form fields.
        labels = {
            "ssn": "Social Security Number (SSN) ",  # Label for SSN input.
            "dob": "Date of Birth",  # Label for date of birth input.
        }

    # Custom validation for the date of birth (dob) field.
    def clean_dob(self):
        dob1 = self.cleaned_data.get("dob")  # Retrieving the date of birth value from the form data.
        if dob1:
            # Calculate the date 18 years ago to ensure the voter is at least 18 years old.
            minimum_date = timezone.now() - timedelta(days=365 * 18)
            # Check if the entered date of birth is more recent than the calculated date (i.e., under 18 years old).
            if dob1 > minimum_date.date():
                raise forms.ValidationError("You must be at least 18 years old.")  # Raise a validation error if under 18.
        return dob1  # Return the cleaned date of birth if valid.

    # Custom validation for the SSN (Social Security Number) field.
    def clean_ssn(self):
        ssn = self.cleaned_data.get("ssn")  # Retrieving the SSN value from the form data.
        # Regular expression pattern to validate the SSN format (XXX-XX-XXXX).
        ssn_pattern = re.compile(r"^\d{3}-\d{2}-\d{4}$")

        # Check if the entered SSN does not match the required format.
        if not ssn_pattern.match(ssn):
            raise forms.ValidationError("Invalid SSN format. Please use XXX-XX-XXXX.")  # Raise an error if SSN is invalid.

        return ssn  # Return the cleaned SSN if valid.


# Defining the form for the Position model, inheriting from FormSettings.
class PositionForm(FormSettings):
    class Meta:
        # Specifies the model and fields for the form.
        model = Position  # This form is based on the Position model.
        fields = ["name", "max_vote"]  # The fields to display and process in the form (name and max_vote).


# Defining the form for the Candidate model, also inheriting from FormSettings.
class CandidateForm(FormSettings):
    class Meta:
        # Specifies the model and fields for the form.
        model = Candidate  # This form is based on the Candidate model.
        fields = ["fullname", "bio", "position", "photo"]  # Fields for candidate's full name, bio, position, and photo.

