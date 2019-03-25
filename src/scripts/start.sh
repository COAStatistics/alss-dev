#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

python manage.py migrate
python manage.py collectstatic --noinput --verbosity 0

echo "from apps.users.tests import initial" | python manage.py shell

python manage.py loaddata fixtures/surveys18/*.yaml
python manage.py loaddata fixtures/surveys18/survey/*.yaml
python manage.py loaddata fixtures/surveys19/*.yaml
python manage.py loaddata fixtures/surveys19/survey/*.yaml

python manage.py runserver 0.0.0.0:8000
