# -*- coding: utf-8 -*-

import logging
import flask_excel as excel

from flask import Flask
from werkzeug.utils import import_string

from backend.client import db, logger
from backend.config import DEBUG
from backend.libs.bputils import get_apis_blueprints

HEADERS = {
    'Access-Control-Max-Age': '1728000',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS, HEAD',
}


def create_backend():
    """create backend function return flask backend instance"""
    backend = Flask(__name__)
    backend.config.from_object('backend.config')
    backend.secret_key = backend.config['SECRET_KEY']

    backend.url_map.strict_slashes = False

    db.init_app(backend)
    excel.init_excel(backend)

    if DEBUG:
        logger.setLevel(logging.DEBUG)

    for (app, bp_name) in get_apis_blueprints():
        import_name = '%s.apps.%s.apis.%s:bp' % (__package__, app, bp_name)
        backend.register_blueprint(import_string(import_name))

    @backend.after_request
    def after_request(resp):
        for k, v in HEADERS.items():
            resp.headers[k] = v

        return resp

    return backend
