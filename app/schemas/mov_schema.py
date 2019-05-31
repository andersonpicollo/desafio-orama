# -*- coding: utf-8 -*-
from marshmallow import Schema, fields


class MovSchema(Schema):

    data = fields.DateTime()
    tipo = fields.String()
    valor = fields.Float()