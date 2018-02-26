# -*- coding: utf-8 -*-
import os
from functools import partial

from flask import Blueprint, jsonify
from flask_jwt import JWTError, jwt_required
from werkzeug.exceptions import HTTPException

from backend.config import DEBUG
from backend.const import BASE_DIR
from backend.libs.exception import CustomError
from backend.libs.jsonutils import jsonize

INTERNAL_SERVER_ERROR = 500
ERROR_CODES = [400, 401, 403, 404, 408]
DEFAULT_RETURN_VALUE = {'error': None}


def get_apis_blueprints(exclude=None):
    if not exclude:
        exclude = []

    apps_dir = os.path.join(BASE_DIR, 'backend/apps')
    api_dirs = [(i, os.path.join(apps_dir, i)) for i in os.listdir(apps_dir)
                if not i.startswith('__')]
    api_dirs = [(a, os.path.join(p, 'apis')) for (a, p) in api_dirs
                if os.path.isdir(p)]

    apis = []
    if not DEBUG:
        exclude = exclude if exclude else []
        exclude.append('test')

    for (app, api_dir) in api_dirs:
        for path in os.listdir(api_dir):
            if path.startswith('__') or not path.endswith('.py'):
                continue

            api = os.path.splitext(path)[0]
            if not api or api in exclude:
                continue

            apis.append((app, api))

    return apis


class URLPrefixError(Exception):
    pass


def patch_blueprint_route(bp):
    origin_route = bp.route

    def patched_route(self, rule, **options):
        def decorator(f):
            origin_route(rule, **options)(jsonize(f))

        return decorator

    bp.route = partial(patched_route, bp)


def create_api_blueprint(name, import_name, url_prefix=None, jsonize=True):
    """方便创建 api blueprint 增加 4xx 请求处理，返回值 json 化
    name, import_name, url_prefix 同 Blueprint
    jsonize 等于 Ture 时，自动帮忙序列化，反之没有处理

    在 debug 模式下，500 的错误不进行处理，走 flask 默认的处理，方便调试

    使用：

    from flask import abort

    abort(404, 'xxx not found')
    request 返回 {'msg': 'xxx not found', 'code': 404}, 200

    # raise 非自定义错误
    raise Exception('xxx')
    request 返回 {'msg': '服务器错误'}, 500

    raise CustomError('error', code, payload)
    request 返回 {'msg': 'error', 'code': 200, payload}, 200

    """

    if url_prefix and url_prefix.startswith('/'):
        raise URLPrefixError(
            'url_prefix ("{}") must not start with /'.format(url_prefix))

    bp_url_prefix = '/api/'
    if url_prefix:
        bp_url_prefix = os.path.join(bp_url_prefix, url_prefix)
    bp = Blueprint(name, import_name, url_prefix=bp_url_prefix)

    def _error_hanlder(error):
        print(error)
        # 处理自定义错误
        if issubclass(error.__class__, CustomError):
            return jsonify(error.to_dict())

        # 处理 abort 错误
        if isinstance(error, HTTPException):
            return jsonify({
                'msg': error.description,
                'code': error.code,
            })

        if isinstance(error, JWTError):
            return jsonify({'msg': error.description, 'code': 401})

        # 处理其他错误
        return jsonify({
            'msg': '服务器错误',
            'code': INTERNAL_SERVER_ERROR,
        }), INTERNAL_SERVER_ERROR

    for code in ERROR_CODES:
        bp.errorhandler(code)(_error_hanlder)

    bp.errorhandler(CustomError)(_error_hanlder)
    bp.errorhandler(JWTError)(_error_hanlder)

    if not DEBUG:
        bp.errorhandler(INTERNAL_SERVER_ERROR)(_error_hanlder)

    if jsonize:
        patch_blueprint_route(bp)

    return bp


def empty(*args, **kwargs):
    """为了 jwt_required 构造的空函数
    """
    return


login_required = jwt_required()(empty)
