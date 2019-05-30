# -*- coding: utf-8 -*-
from sqlalchemy import Column, String
from app.model import Base
from sqlalchemy.orm import relationship


class Cliente(Base):

    """
        Classe ORM para tabela cliente
    """

    nome = Column(String(50), nullable=False)
    cpf = Column(String(14), nullable=False, unique=True)
    email = Column(String(50), nullable=True)
    contas = relationship("Conta")

    def __init__(self, nome, cpf, email):

        self.nome = nome
        self.cpf = cpf
        self.email = email
