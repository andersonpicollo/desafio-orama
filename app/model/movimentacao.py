# -*- coding: utf-8 -*-
from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy import DateTime, func
from app.model import Base


class Movimentacao(Base):

    """
        Classe ORM para Movimentacao
    """

    data = Column(DateTime, nullable=False, default=func.now())
    valor = Column(Float, nullable=False)
    # Substituir por tabela para categorizar os tipos de transaçoes
    tipo = Column(String(50), nullable=False)
    conta_id = Column(Integer, ForeignKey('conta.id'), nullable=False)

    def __init__(self, tipo, conta_id, valor):
        self.tipo = tipo
        self.conta_id = conta_id
        self.valor = valor
