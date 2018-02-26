FROM python:3.6-alpine3.6

ENV PYTHONUNBUFFERED 1
COPY requirements.txt /service/requirements.txt
WORKDIR /service

RUN apk add --no-cache gcc libc-dev jpeg-dev zlib-dev\
    &&pip install -r requirements.txt \
    &&rm -rf /var/cache/apk/* /tmp/* /var/tmp/* $HOME/.cache
