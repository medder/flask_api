#!/bin/bash

source "$(dirname ${BASH_SOURCE[0]})/utils.sh"

ensure ">>> killing existing services" docker-compose kill backend
ensure ">>> removing existing services" docker-compose rm -f -v && docker-compose down

if [ -n "${BUILD}" ]
then
    ensure "building services" docker-compose build
fi

if [ -n "${PULL}" ]
then
    ensure "pulling images" docker-compose pull
fi

ensure ">>> starting services" docker-compose up -d
