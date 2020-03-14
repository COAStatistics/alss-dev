DJANGO_CONTAINER_NAME = web

attach:
	docker exec -it ${DJANGO_CONTAINER_NAME} bash

shell:
	docker exec -it ${DJANGO_CONTAINER_NAME} python manage.py shell

flake8:
	docker exec -it ${DJANGO_CONTAINER_NAME} flake8 --exclude=migrations --ignore=E121,E203,E226,E402,E501,F401,F403,W503 ./