from django import forms  # Importing Django's forms module to create form classes.
from .models import *  # Importing all models from the current app.

# A base form class that customizes form behavior and appearance.
class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Initializing the form using Django's default ModelForm __init__ method.
        super(FormSettings, self).__init__(*args, **kwargs)
        
        # Loop through all the visible fields in the form.
        for field in self.visible_fields():
            # Add the 'form-control' class to each field's widget for Bootstrap styling.
            field.field.widget.attrs['class'] = 'form-control'


# A form class for handling user creation and updating.
class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)  # A required field for the user's email.
    password = forms.CharField(widget=forms.PasswordInput)  # A required password field with input masked as a password.

    # Custom widget dictionary to apply a password input type to the password field.
    widget = {
        'password': forms.PasswordInput(),
    }

    # Custom initialization method to handle dynamic form behaviors (like password placeholders and setting initial data).
    def __init__(self, *args, **kwargs):
        # Call the parent class's __init__ method to ensure the form is set up correctly.
        super(CustomUserForm, self).__init__(*args, **kwargs)

        # If the form is instantiated with an 'instance' (i.e., for updating a user).
        if kwargs.get('instance'):
            instance = kwargs.get('instance').__dict__  # Get the instance's data as a dictionary.
            
            # Set password as not required during updates.
            self.fields['password'].required = False
            
            # Loop through the fields and set their initial data from the instance.
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            
            # If the instance exists (i.e., during an update operation).
            if self.instance.pk is not None:
                # Show a placeholder to indicate that password is optional (only if the user wants to update it).
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"
        else:
            # If no instance is passed (i.e., during a creation), make first_name and last_name required.
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True

    # Custom validation for the email field.
    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()  # Get the email and convert it to lowercase for consistency.
        
        # If the form is being used for creation (no existing instance).
        if self.instance.pk is None:
            # Check if the email already exists in the database.
            if CustomUser.objects.filter(email=formEmail).exists():
                # Raise a validation error if the email is already registered.
                raise forms.ValidationError("The given email is already registered")
        else:  # If the form is being used for an update (existing instance).
            dbEmail = self.Meta.model.objects.get(id=self.instance.pk).email.lower()  # Get the current email in the database.
            
            # If the email has been changed.
            if dbEmail != formEmail:
                # Check if the new email already exists in the database.
                if CustomUser.objects.filter(email=formEmail).exists():
                    # Raise a validation error if the new email is already registered.
                    raise forms.ValidationError("The given email is already registered")
        
        # Return the cleaned email.
        return formEmail

    # Custom validation for the password field.
    def clean_password(self):
        password = self.cleaned_data.get("password", None)  # Get the password from the form data.
        
        # If the form is being used for an update (existing instance).
        if self.instance.pk is not None:
            # If no password is provided during an update, return the current password (i.e., don't change it).
            if not password:
                return self.instance.password

        # Return the hashed version of the password using Django's make_password utility.
        return make_password(password)

    # Meta class to define the model and fields used by this form.
    class Meta:
        model = CustomUser  # Set the form to be based on the CustomUser model.
        fields = ['last_name', 'first_name', 'email', 'password', ]  # Fields to include in the form.

