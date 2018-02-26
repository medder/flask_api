#!/bin/bash

source "$(dirname ${BASH_SOURCE[0]})/utils.sh"

ensure ">>> killing existing services" docker-compose kill backend
ensure ">>> removing existing services" docker-compose rm -f -v && docker-compose down
ensure ">>> starting services" docker-compose run -p 5000:5000 backend python run.py
