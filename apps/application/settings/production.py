from .base import *

# Allow all host headers
ALLOWED_HOSTS = ['falmer.sussexstudent.com']
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
# SECURE_HSTS_SECONDS = 3600 - not yet
X_FRAME_OPTIONS = 'DENY'

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
    'release': os.getenv('HEROKU_SLUG_COMMIT', 'unknown'),
}
