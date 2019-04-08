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

Use `--build` to rebuild image(if requires changes, you must add this), `-d` to run containers in the background:
```
$ docker-compose up
```

Run a command in a running container with bash, `web` is the `container_name` defined in `docker-compose.yaml`:
```
$ docker exec -it web bash
```

Use `-v` to clean volume while stop containers(if migrations files have been rewired, you must add this):
```
$ docker-compose down -v
```


