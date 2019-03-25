# Agriculture Labor Shortage Survey
Provide online survey creation and edition with error examination alerts for investgators and reviewers

## Development with Docker

Setup `src/dashboard/settings/local.py`, with following configurations:
```
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
```

Use `--build` to rebuild image, `-d` to run containers in the background :
```
$ docker-compose up
```

Use `-v` to clean volume while stop containers:
```
$ docker-compose down -v
```


