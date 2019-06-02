# -*- coding: utf-8 -*-

import falcon
from app.resource import ClienteResource
from app.database import init_session
from app.resource import ContaResource
from app.resource import MovResource
from app.middleware import JsonParser
from app.exceptions import AppError

init_session()
middleware = [JsonParser()]
application = api = falcon.API(middleware=middleware)
api.add_route('/clientes', ClienteResource())
api.add_route('/clientes/{cliente_id}', ClienteResource())
api.add_route('/contas', ContaResource())
api.add_route('/contas/{conta_id}', ContaResource())
api.add_route('/movimentacao', MovResource())
api.add_route('/movimentacao/{conta_id}/{date_inicio}/{date_fim}', MovResource())
api.add_error_handler(AppError, AppError.handle)
