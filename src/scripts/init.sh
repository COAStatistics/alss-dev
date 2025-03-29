#!/usr/bin/env bash

echo "from apps.users.tests.initial import create_groups; create_groups();" | python manage.py shell
echo "from apps.users.tests.initial import create_superuser; create_superuser();" | python manage.py shell
echo "from apps.users.tests.initial import create_staff; create_staff();" | python manage.py shell

python manage.py loaddata fixtures/surveys18/*.yaml
python manage.py loaddata fixtures/surveys18/survey/*.yaml
python manage.py loaddata fixtures/surveys19/*.yaml
python manage.py loaddata fixtures/surveys19/survey/670100013471.yaml
python manage.py loaddata fixtures/surveys20/*.yaml
python manage.py loaddata fixtures/surveys20/survey/*.yaml
python manage.py loaddata fixtures/surveys22/*.yaml
python manage.py loaddata fixtures/surveys22/survey/*.yaml
python manage.py loaddata fixtures/surveys23/*.yaml
python manage.py loaddata fixtures/surveys23/survey/*.yaml
python manage.py loaddata fixtures/surveys24/*.yaml
python manage.py loaddata fixtures/surveys24/survey/*.yaml
python manage.py loaddata fixtures/surveys25/*.yaml
python manage.py loaddata fixtures/surveys25/survey/*.yaml