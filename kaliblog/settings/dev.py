from kaliblog.settings.base import *

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# EMAIL CONFIGURATION FOR CONSOLE
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None
EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
