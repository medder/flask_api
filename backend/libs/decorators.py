# -*- coding: utf-8 -*-

import functools
import inspect

from flask import request

from backend.libs.utils import check_params


def query_params(**config):
    """处理、校验 request 参数，并且当做参数传入 api 函数中

    使用:
    1:  所有参数配置 config
        @bp.route(xxx)
        @query_params(page={'default': default, 'type_': int,
                            'required': True, 'min_': 0, 'max_': 999})
        def test(page, count):
            xxx

    2:
        参数不带config，默认值为 None
        @bp.route(xxx)
        @query_params(page={'default': default, 'type_': int,
                            'required': True, 'min_': 0, 'max_': 999})
        def test(page, count, time):
            xxx

    参数:
    default: 默认值(可选)
    type_: 参数类型(可选)
    required: 是否必须，默认为 False (可选)
    min_: 最小值, 如果是字符类型，为长度 (可选)
    max_: 最大值, 如果是字符类型，为长度 (可选)

    异常：
    * 值缺失抛 MissingRequiredField
    * 值校验失败抛 InvalidParameter

    使用 is None 防止 0 值
    """

    def __query_params(func):
        need_params = inspect.getfullargspec(func).args

        @functools.wraps(func)
        def __(*args, **kwargs):
            request_params = request.values

            # 最后返回的参数列表
            params = check_params(
                request_params, config, need_params=need_params, **kwargs)

            return func(**params)

        return __

    return __query_params
