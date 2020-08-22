from .base import *
from .base import INSTALLED_APPS

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

INSTALLED_APPS += ['django_extensions']

NOTEBOOK_ARGUMENTS = [
    # exposes IP and port
    '--ip=0.0.0.0',
    '--port=8888',
    '--allow-root',
    '--NotebookApp.token=""',
]
