# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


def get_engine(uri):
    return create_engine(uri)


# Substituir por arquivo de configuração.
engine = get_engine('postgresql+psycopg2://orama:orama@localhost/desafio-orama')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def init_session():

    Session.configure(bing=engine)
    from app.model import Base
    Base.metadata.create_all(engine)