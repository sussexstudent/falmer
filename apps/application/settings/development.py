from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "0c&qbxs5&2nlwoizqsvn00hrb!+3y)i0-29c_qy%@rvk)%yqnr"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow all host headers
ALLOWED_HOSTS = ['*']

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

PUBLIC_HOST = 'http://localhost:5000'
