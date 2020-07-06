from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': '5432',
    },
}

ADMINS = [
    ('steven', 'tw19900703@hotmail.com'),
	
]

SERVER_EMAIL = 'coa.statistics@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'coa.statistics@gmail.com'
EMAIL_HOST_PASSWORD = 'adminzxcv1234-+'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "COA Statistics <coa.statistics@gmail.com>"
MANAGERS = ADMINS
