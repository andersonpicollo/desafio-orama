# -*- coding: utf-8 -*-

import falcon
from app.resource import ClienteResource
from app.database import init_session
from app.resource import ContaResource
from app.resource import MovResource

init_session()
application = api = falcon.API()
api.add_route('/clientes', ClienteResource())
api.add_route('/clientes/{cliente_id}', ClienteResource())
api.add_route('/contas', ContaResource())
api.add_route('/contas/{conta_id}', ContaResource())
api.add_route('/movimentacao', MovResource())
