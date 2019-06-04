import falcon
import json
from cerberus import Validator
from cerberus.errors import ValidationError
from app.database import Session
from app.schemas import ClienteSchema
from app.model import Conta
from app.model import Cliente
from app.exceptions import InvalidParameterError, ClienteNotExistsError

FIELDS = {

        'nome': {
            'type': 'string',
            'required': True,
            'maxlength': 50
        },
        'cpf': {
            'type': 'string',
            'required': True,
            'maxlength': 14
        },
        'email': {
            'type': 'string',
            'required': True,
            'maxlength': 50
        }
    }


def validate_cliente_request(req, res, resource, params):
    schema = {
        'nome': FIELDS['nome'],
        'cpf': FIELDS['cpf'],
        'email': FIELDS['email']
    }

    validator = Validator(schema)
    validator.allow_unknown = True

    try:
        if not validator.validate(req.context['data']):
            raise InvalidParameterError(validator.errors)
    except ValidationError:
        raise InvalidParameterError('Invalid Request %s' % req.context)


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

    @falcon.before(validate_cliente_request)
    def on_post(self, req, resp):

        req_body = req.context['data']
        if req_body:
            session = Session()
            cliente = Cliente(req_body['nome'], req_body['cpf'], req_body['email'])
            session.add(cliente)
            session.commit()
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(
                {
                    "code": 200,
                    "message": "OK"
                }
            )
            session.close()
        else:
            raise InvalidParameterError(req.context['data'])

    @falcon.before(validate_cliente_request)
    def on_put(self, req, resp):

        req_body = req.context['data']
        if req_body['id']:
            session = Session()
            cliente_update = session.query(Cliente).filter(Cliente.id == req_body['id']).update({"nome": req_body['nome'],
                                                                                      "cpf": req_body['cpf'],
                                                                                      "email": req_body['email']
                                                                            })
            if cliente_update:
                resp.status = falcon.HTTP_200
                session.close()
            else:
                raise ClienteNotExistsError('user id: %s' % req_body['id'])
        else:
            raise InvalidParameterError(req.context['data'])