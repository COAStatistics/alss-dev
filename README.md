# Agriculture Labor Shortage Survey
Provide online survey creation and edition with error examination alerts for investgators and reviewers

## Develop with Docker

Start services, use `--build` to rebuild image(if requires changes, you must add this), `-d` to run containers in the background:
```
$ docker-compose up
```

Attach container with bash, `web` is the `container_name` defined in `docker-compose.yaml`:
```
$ make attach
```

Stop services, Use `-v` to clean volume while stop containers(if migrations files have been rewired, you must add this):
```
$ docker-compose down -v
```

## IPython Notebook

For convenience, spawn a jupyter notebook service at [localhost:8888](http://localhost:8888). The files are ignored in version control.


## Testing

Attach the web container before running tests, available mark are list in [pytest.ini](src/pytest.ini)
```
pytest -m [Mark]
```
