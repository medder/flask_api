# -*- coding: utf-8 -*-

import json
from datetime import datetime, time
from decimal import Decimal
from functools import wraps

from flask import Response
from flask_sqlalchemy import Pagination


class Jsonized(object):

    _raw = {}

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def to_dict(self):
        return self._raw


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Jsonized):
            return obj.to_dict()
        if isinstance(obj, str):
            return obj.encode('utf-8')
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, time):
            return obj.strftime('%H:%M')
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, Pagination):
            return {
                "result": obj.items,
                "current": obj.page,
                "total": obj.pages,
                "total_count": obj.total
            }
        return super(JSONEncoder, self).default(obj)


def jsonize(f):
    @wraps(f)
    def _(*args, **kwargs):
        r = f(*args, **kwargs)
        data, code = r if isinstance(r, tuple) else (r, 200)

        # 处理下载时不需要json化的代码
        if isinstance(data, Response):
            return data

        data = {
            'code': 200,
            'msg': 'success',
            'data': data,
        }
        return Response(
            json.dumps(data, cls=JSONEncoder),
            status=code,
            mimetype='application/json')

    return _
