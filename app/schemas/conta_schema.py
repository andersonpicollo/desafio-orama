# -*- coding: utf-8 -*-
from marshmallow import Schema, fields
from app.schemas import MovSchema


class ContaSchema(Schema):
    numero = fields.String()
    saldo = fields.Float()
    mov = fields.Nested(MovSchema(), many=True)

