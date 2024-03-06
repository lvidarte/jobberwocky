#!/bin/bash

source bin/config.sh

if [[ ! -d "$PY_ENV" ]]; then
  echo "Python environment ${PY_ENV} does not exist! creating..."
  python3 -m venv $PY_ENV
  source $PY_ENV/bin/activate
  pip install --upgrade pip
  pip install --no-cache-dir -r requirements.txt
  deactivate
fi
