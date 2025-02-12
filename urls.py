from django.urls import path  # Importing Django's 'path' function to define URL patterns.
from . import views  # Importing all the views from the current app (account).
from voting.views import account_download_key  # Importing 'account_download_key' from the 'voting' app's views.

# Defining the URL patterns for the 'account' app.
urlpatterns = [
    # Root URL ('') mapped to 'account_login' view, which handles user login. The URL name is "account_login".
    path('', views.account_login, name="account_login"),
    
    # URL for user registration ('/register/'), mapped to 'account_register' view. The URL name is "account_register".
    path('register/', views.account_register, name="account_register"),
    
    # URL for logging out ('/logout/'), mapped to 'account_logout' view. The URL name is "account_logout".
    path('logout/', views.account_logout, name="account_logout"),
    
    # URL for downloading the key ('/keydownload/'), mapped to 'account_download_key' view from the 'voting' app. The URL name is "account_download_key".
    path('keydownload/', account_download_key, name="account_download_key"),
]

