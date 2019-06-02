# -*- coding: utf-8 -*-
from marshmallow import Schema, fields



class MovSchema(Schema):

    created = fields.Date()
    tipo = fields.String()
    valor = fields.Float()
