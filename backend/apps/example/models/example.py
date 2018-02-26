# -*- coding: utf-8 -*-
"""样例model"""

from backend.client import db
from backend.libs.model import BaseModelMixin


class Example(BaseModelMixin):
    """样例model
    """
    # 邮箱
    email = db.Column(
        db.String(50),
        nullable=False,
        info=dict(creatable=True, editable=True))
    # 用户名称
    name = db.Column(
        db.String(50),
        info=dict(creatable=True, editable=True))
