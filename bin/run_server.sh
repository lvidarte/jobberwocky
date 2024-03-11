#!/bin/bash

source bin/config.sh

bin/create_env.sh

source $PY_ENV/bin/activate
cd jobberwocky

echo "Running server!"

export JOBBERWOCKY_LOG_LEVEL="DEBUG"
export JOBBERWOCKY_APP_URL="http://localhost:8000"
export JOBBERWOCKY_DATABASE_URL="sqlite:///jobberwocky.db"
export JOBBERWOCKY_EXTRA_SOURCE_URL="http://localhost:8080/jobs"
export JOBBERWOCKY_EXTRA_SOURCE_TIMEOUT="3"
export JOBBERWOCKY_MAILGUN_DOMAIN=""
export JOBBERWOCKY_MAILGUN_API_KEY=""
uvicorn main:app --reload-dir . --reload-dir tests --log-config=logconf.yaml

cd - >/dev/null
deactivate
