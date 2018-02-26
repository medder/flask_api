# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_PAGE = 1
DEFAULT_COUNT_PRE_PAGE = 10
DEFAULT_SORT = '-id'

PAGE_COUNT_PARAMS = {
    'page': {
        'default': DEFAULT_PAGE,
        'type_': int
    },
    'count': {
        'default': DEFAULT_COUNT_PRE_PAGE,
        'type_': int
    },
    'sort': {
        'default': DEFAULT_SORT,
        'type_': str
    },
}

# 机器修改操作人
MACHINE_EDITOR = 'machine'

BATCH_DELETE_PARAMS = {
    'ids': {
        'required': True,
        'type_': list,
        'list_content_type': int,
    }
}
