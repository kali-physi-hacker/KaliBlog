from kaliblog.settings.base import *

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'kaliblog.herokuapp.com']

SECRET_KEY = os.environ.get('SECRET_KEY', 'not-so-secret-key')

DEBUG = int(os.environ.get('DEBUG', default=1))

# DATABASE CONFIGURATION
import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500

# EMAIL CONFIGURATION FOR GMAIL SMTP
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'brownjunior956@gmail.com'
EMAIL_HOST_PASSWORD = 'BLACKFOXA1B2C3IQ'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
