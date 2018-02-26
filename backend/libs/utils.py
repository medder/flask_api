# -*- coding: utf-8 -*-

from collections import Sequence
from datetime import datetime
from functools import wraps

from flask import request

from backend.libs.exception import (InvalidParameter, MissingRequiredField,
                                    NoData)


def params_parse(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = {}
        for key in request.args:
            data[key] = request.args.get(key)

        if data:
            kwargs.update(data)
        return func(*args, **kwargs)

    return wrapper


def check_params(data, config, need_params=None, **kwargs):
    """参数校验
    使用:
        TODO

    参数说明:
    data: 传入的data
    config: 配置每个参数校验的规则
    need_parmas: 需要检验的参数，可与config配合使用,
                 比如在@query_params(**PAGE_COUNT_PARAMS)中的使用

    config参数定义规则:
    default: 默认值(可选)
    type_: 参数类型(可选)
    required: 是否必须，默认为 False (可选)
    min_: 最小值, 如果是字符类型，为长度 (可选)
    max_: 最大值, 如果是字符类型，为长度 (可选)
    data_fmt: 需要装换的数据格式
    only_time: 转成datetime.time格式

    异常：
    * 值缺失抛 MissingRequiredField
    * 值校验失败抛 InvalidParameter

    使用 is None 防止 0 值
    """
    if data is None:
        raise NoData()

    if not need_params:
        need_params = config.keys()

    # 最后返回的参数列表
    params = {}

    for param in need_params:
        val = data.get(param)
        if val is None:
            val = kwargs.get(param)

        conditions = config.get(param)

        # 如果没有 config，不做任何处理，默认值就是 None
        if not conditions:
            params[param] = val
            continue

        # 检查是否必须
        if conditions.get('required', False):
            flag = isinstance(val, (Sequence, dict, set)) and not val
            if val is None or flag:
                raise MissingRequiredField(param)

        # 检查是否有默认值
        default = conditions.get('default')
        if default is not None and val is None:
            params[param] = default
            continue

        # 字符串转时间
        date_fmt = conditions.get('date_fmt')
        if date_fmt:
            try:
                if conditions.get('only_time', False):
                    val = datetime.strptime(val, date_fmt).time()
                else:
                    val = datetime.strptime(val, date_fmt)
            except ValueError:
                # 如果是必须值，那就返回错误，否则使用默认值（在default时没检测到是因为val为"", 非None）
                raise InvalidParameter(param)
        # 检查类型是否正确，避免使用 type 关键字
        type_ = conditions.get('type_')
        if type_:

            if not isinstance(val, type_):
                try:
                    val = type_(val)
                except ValueError:
                    raise InvalidParameter(param)

            list_content_type = conditions.get('list_content_type')
            if type_ == list and list_content_type:
                try:
                    val = [list_content_type(i) for i in val]
                except ValueError:
                    raise InvalidParameter(param)

        # 检查范围，如果字符类型比较长度，否则比较数值本身
        min_ = conditions.get('min_')
        max_ = conditions.get('max_')
        if not any([min_, max_]):
            params[param] = val
            continue

        v_min = v_max = val
        if isinstance(val, (str, bytes)):
            v_min = v_max = len(val)

        # 数组只提供内容非字符串的比较
        elif isinstance(val, list) and list_content_type == int:
            v_max = max(val)
            v_min = min(val)

        if (min_ and v_min < min_) or (max_ and v_max > max_):
            raise InvalidParameter(param)

        params[param] = val

    return params
