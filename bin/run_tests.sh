#!/bin/bash

source bin/config.sh

bin/create_env.sh

source $PY_ENV/bin/activate
cd jobberwocky

if [[ -f "$DB_TESTS" ]]; then
  echo "Removing database for tests '$DB_TESTS' ..."
  rm $DB_TESTS
fi

echo "Running tests!"

export PYTHONWARNINGS="ignore"
export JOBBERWOCKY_LOG_LEVEL="CRITICAL"
export JOBBERWOCKY_APP_URL=""
export JOBBERWOCKY_DATABASE_URL="sqlite:///${DB_TESTS}"
export JOBBERWOCKY_EXTRA_SOURCE_URL="http://localhost:8080/jobs"
export JOBBERWOCKY_EXTRA_SOURCE_TIMEOUT="3"
export JOBBERWOCKY_MAILGUN_DOMAIN=""
export JOBBERWOCKY_MAILGUN_API_KEY=""
python -m unittest discover tests

cd - >/dev/null
deactivate
