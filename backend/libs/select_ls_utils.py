# -*- coding: utf-8 -*-

import ast

from sqlalchemy import or_

PAGE_NO_DEFAULT = 1
PAGE_COUNT_DEFAULT = 10000


def _order_parse(cls, d):
    """将{'id': 'desc'}转换为Publisher.id.desc(), 支持多字段排序
    """
    order_ls = []
    for k, v in d.items():
        filed_ob = getattr(cls, k)
        order_pa = getattr(filed_ob, v)()
        order_ls.append(order_pa)

    return order_ls


def _search_parse(cls, search_content, search_column):
    search_ls = []
    for s in search_column:
        filed_ob = getattr(cls, s)
        search_ls.append(
            filed_ob.like("%{0}%".format(search_content.encode('utf-8'))))

    return search_ls


def get_ls(cls, page_no, page_count, filter_condition, order_condition,
           search_content, search_column):
    """分页、排序、删除、搜索的公共接口.
    使用方法:
    page_no: int
    page_count: int
    filter_condition: {'name': 'zhangsan', 'sex': 1}
    order_condition: {'id': 'desc', 'name': 'asc'}
    search_content: 'zhansan'
    search_column: ['id', 'name', 'sex']
    """
    order_p = _order_parse(cls, order_condition)

    search_p = _search_parse(cls, search_content, search_column)

    pagination = cls.query.filter_by(
        **filter_condition).order_by(*order_p).filter(or_(*search_p)).paginate(
            page_no, per_page=page_count, error_out=False)

    items = pagination.items
    total = pagination.total

    return items, total


def get_select_info(args):
    """筛选的信息
    """
    try:
        page_no = int(args.get('page_no', PAGE_NO_DEFAULT))
        page_count = int(args.get('page_count', PAGE_COUNT_DEFAULT))

        filter_condition = args.get('filter_condition', '{}')
        filter_condition = ast.literal_eval(filter_condition)

        order_condition = args.get('order_condition', '{}')
        order_condition = ast.literal_eval(order_condition)

        search_content = args.get('search_content', '')

        search_column = args.get('search_column', '[]')
        search_column = ast.literal_eval(search_column)
    except Exception as e:
        raise e

    return (page_no, page_count, filter_condition, order_condition,
            search_content, search_column)
