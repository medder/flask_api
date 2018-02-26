# -*- coding: utf-8 -*-

from enum import Enum, unique

from flask_sqlalchemy import Pagination
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.inspection import inspect
from sqlalchemy import or_

from backend.client import db
from backend.const import DEFAULT_COUNT_PRE_PAGE, DEFAULT_PAGE, DEFAULT_SORT
from backend.libs.exception import (InvalidParameter, MissingRequiredField,
                                    ObjectNotFound, ProhibitEditField)
from backend.libs.jsonutils import Jsonized

CREATED_AT_DEFAULT_VAL = 'CURRENT_TIMESTAMP'
UPDATED_AT_DEFAULT_VAL = 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'


@unique
class Status(Enum):
    DELETED = 0
    ONLINE = 1


VALID_STATUS = {s.value for s in Status if s != Status.DELETED}


class BaseModelMixin(Jsonized, db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.SmallInteger, default=Status.ONLINE.value)
    created_at = db.Column(
        db.TIMESTAMP(True),
        nullable=False,
        server_default=db.text(CREATED_AT_DEFAULT_VAL))
    updated_at = db.Column(
        db.TIMESTAMP(True),
        nullable=False,
        server_default=db.text(UPDATED_AT_DEFAULT_VAL))

    @property
    def return_fields(self):
        return self.__table__.columns.keys()

    @classmethod
    def required_fields(cls):
        return [
            f for f, v in cls.__table__.columns.items()
            if getattr(v, 'info', {}).get('creatable')
        ]

    @classmethod
    def editable_fields(cls):
        return [
            f for f, v in cls.__dict__.items()
            if getattr(v, 'info', {}).get('editable')
        ]

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.get_id())

    def __eq__(self, other):
        is_same_id = self.get_id() == other.get_id()
        return isinstance(other, self.__class__) and is_same_id

    def to_dict(self):
        return {field: getattr(self, field) for field in self.return_fields}

    def get_id(self):
        """获取主键的值
        """
        identity = inspect(self).identity
        return identity[0] if identity else None

    @staticmethod
    def commit():
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise e

    @classmethod
    def __get_by_id(cls, id, force=True):
        self = super().query.get(id)
        if self and self.status != Status.DELETED.value:
            return self

        if force:
            raise ObjectNotFound(cls.__name__, id)

        return None

    @classmethod
    def get_by_id(cls, id, force=True):
        return cls.__get_by_id(id, force)

    @hybrid_property
    def query(self):
        return super().query.filter(self.status != Status.DELETED.value)

    @classmethod
    def delete(cls, id):
        self = cls.__get_by_id(id, True)

        self.status = Status.DELETED.value

        if getattr(cls, 'relations', None):
            for foreign_key in cls.relations:
                foreign_key.class_.delete_by_foreign(foreign_key, id)

        cls.commit()
        return self

    @classmethod
    def batch_delete(cls, ids):
        objs = cls.query.filter(cls.id.in_(ids))
        for obj in objs:
            obj.status = Status.DELETED.value
        cls.batch_save(objs)
        return 'OK'

    @classmethod
    def delete_by_foreign(cls, foreign_key, id):
        cls.query.filter(foreign_key == id).update(
            dict(status=Status.DELETED.value))

    @classmethod
    def update(cls, id, *args, **kwargs):
        self = cls.__get_by_id(id)

        for key in cls.editable_fields():
            val = kwargs.pop(key, None)
            if val is not None:
                setattr(self, key, val)

        if kwargs:
            for key, val in kwargs.items():
                print(getattr(self, key, None), val)
                if getattr(self, key, None) == val:
                    continue

                raise ProhibitEditField(', '.join(kwargs.keys()))

        cls.commit()

        return self

    @classmethod
    def update_status(cls, id, status):
        self = cls.get_by_id(id)

        if status is None or int(status) not in VALID_STATUS:
            raise InvalidParameter('status')

        self.status = status

        cls.commit()

        return self

    @classmethod
    def get_all(cls,
                page=DEFAULT_PAGE,
                count=DEFAULT_COUNT_PRE_PAGE,
                sort=DEFAULT_SORT,
                filters=None,
                search=None):
        items = cls.query

        if filters:
            for key, condition in filters.items():
                if condition is None:
                    continue

                if 'min' in key:
                    key = key.split('_min')[0]
                    items = items.filter(getattr(cls, key) >= condition)
                elif 'max' in key:
                    key = key.split('_max')[0]
                    items = items.filter(getattr(cls, key) <= condition)
                else:
                    items = items.filter(getattr(cls, key) == condition)

        if search:
            search_content = search.pop('search_content')
            search_column = search.pop('search_column')

            search_ls = []
            for s in search_column:
                filed_ob = getattr(cls, s)
                search_ls.append(
                    filed_ob.like("%{0}%".format(
                        search_content)))

            items = items.filter(or_(*search_ls))

        if sort:
            order_by = getattr(cls, sort.strip('-'))
            if sort.startswith('-'):
                order_by = order_by.desc()

            items = items.order_by(order_by)

        if page == 0:
            items = items.all()
            total = len(items)
            return Pagination(None, 1, total, total, items)

        return items.paginate(page, count, False)

    @classmethod
    def create(cls, *args, **kwargs):
        model = cls.gene_obj(cls, *args, **kwargs)
        model.save()

        return model

    @classmethod
    def gene_obj(cls, *args, **kwargs):
        """只生成对象，不提交到数据库"""
        fields = {}
        for field in cls.required_fields():
            val = kwargs.pop(field, None)
            # 避免 val 是 0 或者 ''
            if val is None:
                raise MissingRequiredField(field)

            fields[field] = val

        if kwargs:
            raise ProhibitEditField(', '.join(kwargs.keys()))

        model = cls(**fields)
        return model

    @classmethod
    def batch_save(cls, objs):
        """批量提交
        """
        try:
            db.session.add_all(objs)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_all_obj(cls):
        """获取所有的对象列表
        """
        return cls.query

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise e
