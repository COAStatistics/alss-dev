#!/usr/bin/env bash

echo "from apps.users.tests.initial import create_groups; create_groups();" | python manage.py shell
echo "from apps.users.tests.initial import create_superuser; create_superuser();" | python manage.py shell
echo "from apps.users.tests.initial import create_staff; create_staff();" | python manage.py shell
echo "from apps.users.tests.initial import create_auditor106; create_auditor106();" | python manage.py shell
echo "from apps.users.tests.initial import create_auditor107; create_auditor107();" | python manage.py shell

python manage.py loaddata fixtures/surveys18/*.yaml
python manage.py loaddata fixtures/surveys18/survey/*.yaml
python manage.py loaddata fixtures/surveys19/*.yaml
python manage.py loaddata fixtures/surveys19/survey/670100013471.yaml
python manage.py loaddata fixtures/surveys20/*.yaml
python manage.py loaddata fixtures/surveys20/survey/*.yaml