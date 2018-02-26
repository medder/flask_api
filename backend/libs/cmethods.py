# -*- coding: utf-8 -*-
"""一些公共的方法
"""

import hashlib


def md5_str(key_str):
    """md5加密方法
    加盐
    """
    hash = hashlib.md5()
    key_str = str(key_str) + 'salt'
    hash.update(key_str.encode('utf-8'))
    return hash.hexdigest()


def get_ip_form_request(r):
    if not r:
        return None

    ip = r.headers.get('X-Forwarded-For') or r.remote_addr

    if ip.find(",") != -1:
        ip = ip.split(',')[1]

    return ip
