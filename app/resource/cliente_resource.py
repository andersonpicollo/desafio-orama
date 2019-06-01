import falcon
import json
from app.database import Session
from app.schemas import ClienteSchema
from app.model import Conta
from app.model import Cliente


class ClienteResource(object):

    def on_get(self, req, resp, cliente_id=None):

        session = Session()
        cliente_schema = ClienteSchema()

        if cliente_id:
            cliente = session.query(Cliente).outerjoin(Conta, Cliente.contas).filter(Cliente.id == cliente_id).one()
            payload = cliente_schema.dump(cliente).data

        else:
            clientes = session.query(Cliente).outerjoin(Conta, Cliente.contas).all()
            payload = []
            for cliente in clientes:
                model_to_schema = cliente_schema.dump(cliente).data
                payload.append(model_to_schema)

        resp.body = json.dumps(payload, sort_keys=True)
        resp.status = falcon.HTTP_200
        session.close

    def on_post(self, req, resp):
        session = Session()
        req_body = json.loads(req.stream.read())
        cliente = Cliente(req_body['nome'], req_body['cpf'], req_body['email'])
        session.add(cliente)
        session.commit()
        resp.status = falcon.HTTP_201
        session.close()

    def on_put(self, req, resp):

        session = Session()
        req_body = json.loads(req.stream.read())
        cliente = session.query(Cliente).filter(Cliente.id == req_body['id']).update({"nome": req_body['nome'],
                                                                                      "cpf": req_body['cpf'],
                                                                                      "email": req_body['email']
                                                                                      })
        session.commit()
        resp.status = falcon.HTTP_200
        session.close()



