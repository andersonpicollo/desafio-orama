# -*- coding: utf-8 -*-
from marshmallow import Schema, fields
from app.schemas import ContaSchema


class ClienteSchema(Schema):
    id = fields.Integer()
    nome = fields.String()
    cpf = fields.String()
    email = fields.String()
    contas = fields.Nested(ContaSchema(), many=True)