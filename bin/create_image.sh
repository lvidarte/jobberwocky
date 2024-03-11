#!/bin/bash

set -e

bin/run_tests.sh

docker build --no-cache -t jobberwocky:latest .
