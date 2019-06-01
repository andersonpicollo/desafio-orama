# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from app.model import Base
from sqlalchemy.orm import relationship


class Conta(Base):

    numero = Column(String(10), nullable=True)
    saldo = Column(Float(2))
    tipo = Column(String(50), nullable=False)
    cliente_id = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    mov = relationship("Movimentacao")

    def __init__(self, tipo, numero, cliente_id):
        self.tipo = tipo
        self.numero = numero
        self.saldo = 0
        self.cliente_id = cliente_id
