from kaliblog.settings.base import *


ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DEBUG = True


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'webmaster',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# EMAIL CONFIGURATION FOR GMAIL SMTP
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'brownjunior956@gmail.com'
EMAIL_HOST_PASSWORD = 'BLACKFOXA1B2C3IQ'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
