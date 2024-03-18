#!/bin/bash

bin/create_image.sh

docker pull aquasec/trivy

docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy --severity=HIGH,CRITICAL image jobberwocky:latest 2>/dev/null
