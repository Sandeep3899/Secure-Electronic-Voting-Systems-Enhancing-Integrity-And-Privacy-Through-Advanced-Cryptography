# This docstring explains that this file contains the settings for the `e_voting` project
# It includes links to Django's documentation for further reference.

from pathlib import Path  # Importing Path to handle filesystem paths.
import os  # Importing os to interact with the operating system.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR represents the root directory of the project (the parent directory of the current file's directory).

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%6lp_p!%r$7t-2ql5hc5(r@)8u_fc+6@ugxcnz=h=b(fn#3$p9'
# This is the secret key for cryptographic signing. It should be kept secure and never shared.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG mode is set to True, which is fine for development but should be set to False in production.

ALLOWED_HOSTS = []
# ALLOWED_HOSTS defines which domains or IP addresses are allowed to serve the Django app. 
# It is empty for development, but should be filled with the actual domain or IP in production.

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',  # Django's admin interface.
    'django.contrib.auth',  # Authentication system.
    'django.contrib.contenttypes',  # Handles content types.
    'django.contrib.sessions',  # Manages user sessions.
    'django.contrib.messages',  # Handles messaging framework.
    'django.contrib.staticfiles',  # Manages static files (CSS, JS, images).

    # My Created Applications
    'account.apps.AccountConfig',  # Custom 'account' app.
    'voting.apps.VotingConfig',  # Custom 'voting' app.
    'administrator.apps.AdministratorConfig',  # Custom 'administrator' app.
]
# INSTALLED_APPS lists all the apps and Django components that are used in the project.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Middleware for handling security headers.
    'django.contrib.sessions.middleware.SessionMiddleware',  # Manages user sessions.
    'django.middleware.common.CommonMiddleware',  # Handles common functionalities like URL rewriting.
    'django.middleware.csrf.CsrfViewMiddleware',  # Provides Cross-Site Request Forgery protection.
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Associates users with requests.
    'django.contrib.messages.middleware.MessageMiddleware',  # Manages message framework.
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Provides clickjacking protection.

    'account.middleware.AccountCheckMiddleWare',  # Custom middleware to check user account access.
]
# MIDDLEWARE is a list of all the middleware components that are used to process requests.

ROOT_URLCONF = 'e_voting.urls'
# ROOT_URLCONF points to the root URL configuration for this project. This refers to the `urls.py` file.

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # The template engine used is Django's default.
        'DIRS': ['voting/templates', 'administrator/templates'],  # Custom directories for templates.
        'APP_DIRS': True,  # Automatically looks for templates in app directories.
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Adds debug context if in DEBUG mode.
                'django.template.context_processors.request',  # Adds the request object to the context.
                'django.contrib.auth.context_processors.auth',  # Adds user and authentication context.
                'django.contrib.messages.context_processors.messages',  # Adds messages context.
                'voting.context_processors.ElectionTitle'  # Custom context processor for the election title.
            ],
        },
    },
]
# TEMPLATES configures how Django loads and renders templates.

WSGI_APPLICATION = 'e_voting.wsgi.application'
# WSGI_APPLICATION points to the WSGI configuration for deploying this project.

# Database configuration
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    #   You can use this :
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite is the default database for development.
        'NAME': BASE_DIR / 'db.sqlite3',  # SQLite database will be stored at the root of the project.
    }

    # Example configuration for MySQL (commented out):
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',  # Use MySQL database engine.
    #     'NAME': 'e_voting',  # Name of the MySQL database.
    #     'HOST': '127.0.0.1',  # Database host (localhost).
    #     'USER': 'root',  # MySQL database username.
    #     'PASSWORD': ''  # MySQL password (should be provided in production).
    # }
}
# DATABASES defines the database configurations. By default, it is set to use SQLite for development.

# Password validation settings
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Prevents use of personal info in passwords.
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Enforces a minimum length for passwords.
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Prevents common passwords from being used.
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Prevents all-numeric passwords.
    },
]
# AUTH_PASSWORD_VALIDATORS ensures that user passwords meet certain security requirements.

# Internationalization settings
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'en-us'  # Default language set to English (US).
TIME_ZONE = 'UTC'  # Default timezone is set to UTC.
USE_I18N = True  # Enables internationalization support.
USE_L10N = True  # Enables localization (formats dates, numbers, etc. based on the locale).
USE_TZ = True  # Enables timezone-aware datetimes.

# Static files configuration (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'  # URL to access static files in the browser.

MEDIA_URL = '/media/'  # URL to access media files (like user uploads).
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Directory on the file system where media files will be stored.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')  # Specifies directories for additional static files.
]

# Custom user model and authentication backend settings
AUTH_USER_MODEL = 'account.CustomUser'  # Specifies the custom user model to be used for authentication.
AUTHENTICATION_BACKENDS = ['account.email_backend.EmailBackend']  # Specifies the custom email backend for user authentication.

# Custom file path for storing the election title
ELECTION_TITLE_PATH = os.path.join(
    BASE_DIR, 'election_title.txt')  # Path to store a file that holds the election title.

