from django.urls import path  # Importing the 'path' function to define URL patterns in Django.
from . import views  # Importing views from the current app, which will handle the URL requests.

# Defining URL patterns for the voting app.
urlpatterns = [
    # The root URL ("") is mapped to the 'index' view. When users visit the homepage ("/"), this view is triggered.
    path("", views.index),

    # This URL handles fetching the ballot (with controls). The 'fetch_ballot' view will handle requests to "/ballot/fetch/".
    path("ballot/fetch/", views.fetch_ballot, name="fetch_ballot"),

    # The URL "/dashboard/" maps to the 'dashboard' view, which displays the voter's dashboard. The URL name is "voterDashboard".
    path("dashboard/", views.dashboard, name="voterDashboard"),

    # The URL "/ballot/vote" maps to the 'show_ballot' view, where voters can view the ballot. The URL name is "show_ballot".
    path("ballot/vote", views.show_ballot, name="show_ballot"),

    # The URL "/ballot/vote/preview" allows voters to preview their votes before submission. The 'preview_vote' view handles this. The URL name is "preview_vote".
    path("ballot/vote/preview", views.preview_vote, name="preview_vote"),

    # The URL "/ballot/vote/submit" is where voters submit their final ballot. The 'submit_ballot' view handles this. The URL name is "submit_ballot".
    path("ballot/vote/submit", views.submit_ballot, name="submit_ballot"),

    # The URL "/viewvote" maps to the 'viewvote' view, where voters can see the details of the vote they cast. The URL name is "viewvote".
    path("viewvote", views.viewvote, name="viewvote"),
]

