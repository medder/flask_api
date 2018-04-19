# -*- coding: utf-8 -*-

from flask import abort, request

from backend.const import PAGE_COUNT_PARAMS
from backend.libs.bputils import create_api_blueprint
from backend.libs.decorators import query_params
from backend.libs.exception import ObjectNotFound

from backend.apps.example.models.example import Example

bp = create_api_blueprint('test', __name__, url_prefix='test')


@bp.route('/hello', methods=['GET'])
def hello():
    return 'Hello, World！'


@bp.route('/test', methods=['GET'])
def test():
    abort(400, '出错误了')


@bp.route('/fatal', methods=['GET'])
def fatal():
    how = request.args.get('how')

    if how == '404':
        raise ObjectNotFound('test', 1)

    raise Exception('😆')


@bp.route('/params/<int:id>', methods=['GET'])
@query_params(**PAGE_COUNT_PARAMS)
def test_params(id, page, count, time):
    return {'id': id, 'page': page, 'count': count, 'time': time}


@bp.route('/mysql', methods=['GET'])
def test_mysql():
    return Example.create(email='t_email', name='t_name', city='t_city')
