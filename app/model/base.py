# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer
from sqlalchemy import DateTime, func,Date
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class BaseModel(object):

    # Columns comuns a todas as entidades do sistema.

    id = Column(Integer, primary_key=True)
    created = Column(Date, default=func.now())
    modified = Column(Date, default=func.now(), onupdate=func.now())

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()


Base = declarative_base(cls=BaseModel)
