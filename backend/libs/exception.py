# -*- coding: utf-8 -*-


class CustomError(Exception):
    """自定义错误的基类
    使用
    > raise CustomError('error', 4xx|5xx, payload)
    """
    status_code = 400

    def __init__(self, error, status_code=None, payload=None):
        self.error = error
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['msg'] = self.error
        rv['code'] = self.status_code
        return rv


class NoData(CustomError):
    status_code = 400

    def __init__(self):
        error = 'no data'
        super().__init__(error, self.status_code)


class ObjectNotFound(CustomError):
    status_code = 404

    def __init__(self, obj, id):
        error = '{}: {} 没有找到'.format(obj, id)
        super().__init__(error, self.status_code)


class ObjectExist(CustomError):
    status_code = 400

    def __init__(self, obj, id):
        error = '{}: {} 已经存在'.format(obj, id)
        super().__init__(error, self.status_code)


class MissingRequiredField(CustomError):
    def __init__(self, filed):
        error = '{} is missing'.format(filed)
        super().__init__(error)


class InvalidParameter(CustomError):
    def __init__(self, parameter=None):
        error = 'invalid parameter {}'.format(parameter)
        super().__init__(error)


class ProhibitEditField(CustomError):
    def __init__(self, parameter=None):
        error = 'prohibit edit or no {} field'.format(parameter)
        super().__init__(error)


class CanNotDelete(CustomError):
    def __init__(self, obj=None):
        error = '{} 存在依赖不能删除'.format(obj)
        super().__init__(error)


class StartTBigEndT(CustomError):
    def __init__(self):
        error = '开始时间不能大于结束时间。'
        super().__init__(error)


class UpdatePhotoError(CustomError):
    """ 调用研发修改 photo 状态、点赞，请求错误处理
    """

    def __init__(self, error, status_code):
        super().__init__(error, status_code)
