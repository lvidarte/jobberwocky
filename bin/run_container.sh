#!/bin/bash

bin/create_image.sh

docker run -p 8000:8000 \
  --rm \
  --name jobberwocky \
  --env JOBBERWOCKY_LOG_LEVEL="WARNING" \
  --env JOBBERWOCKY_APP_URL="http://localhost:8000" \
  --env JOBBERWOCKY_DATABASE_URL="sqlite:///jobberwocky.db" \
  --env JOBBERWOCKY_EXTRA_SOURCE_URL="http://172.17.0.3:8080/jobs" \
  --env JOBBERWOCKY_MAILGUN_DOMAIN="" \
  --env JOBBERWOCKY_MAILGUN_API_KEY="" \
  jobberwocky:latest
