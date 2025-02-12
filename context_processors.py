from django.conf import settings  # Importing the settings module from Django to access project-wide settings.

# Defining a function named ElectionTitle that will return the election title as part of the context.
# It accepts 'request' as a parameter, making it suitable for use in views or templates (via context processors).
def ElectionTitle(request):
    context = {}  # Initializing an empty dictionary 'context' to store the election title later.

    title = "No Title Yet"  # Default title in case no election title is found or an error occurs.

    try:
        # Trying to open the file located at the path specified by 'ELECTION_TITLE_PATH' in settings.
        file = open(settings.ELECTION_TITLE_PATH, 'r')
        # Reading the content of the file, which presumably contains the election title.
        title = file.read()
    except:
        # If an error occurs (like the file not existing or being inaccessible), the 'except' block is triggered.
        # In that case, the default title ("No Title Yet") will be used.
        pass

    # Adding the title (either the read title or the default one) to the context dictionary under the key 'TITLE'.
    context['TITLE'] = title

    # Returning the context dictionary, which can be used in views or templates.
    return context

