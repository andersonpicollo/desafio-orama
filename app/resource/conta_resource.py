import falcon
import json
from cerberus import Validator
from cerberus.errors import ValidationError
from app.database import Session
from app.schemas import ContaSchema
from app.model import Conta
from app.model import Movimentacao
from app.exceptions import InvalidParameterError, ClienteNotExistsError

FIELDS = {

    'tipo': {
        'type': 'string',
        'required': True,
        'allowed': ['carteira', 'credito', 'poupanca', 'investimento', 'outro'],
    },

    'numero': {
        'type': 'string',
        'required': True,
        'maxlength': 25
    },

    'cliente_id': {
        'type': 'integer',
        'required': True
    }
}


def validate_conta_request(req, res, resource, params):
    schema = {
        'tipo': FIELDS['tipo'],
        'numero': FIELDS['numero'],
        'cliente_id': FIELDS['cliente_id']
    }

    validator = Validator(schema)
    try:
        if not validator.validate(req.context['data']):
            raise InvalidParameterError(validator.errors)
    except ValidationError:
        raise InvalidParameterError('Invalid Request %s' % req.context)


class ContaResource(object):

    #Lista todas ou uma conta
    def on_get(self, req, resp, conta_id=None):

        """
        :param req: objeto request http
        :param resp: objeto response
        :param conta_id: identificao da conta
        :return: payload json
        """

        session = Session()
        conta_schema = ContaSchema()

        if not conta_id:

            contas = session.query(Conta).outerjoin(Movimentacao, Conta.mov).all()
            payload = []
            for conta in contas:
                model_to_schema = conta_schema.dump(conta).data
                payload.append(model_to_schema)
        else:
            conta = session.query(Conta).outerjoin(Movimentacao, Conta.mov).filter(Conta.id == conta_id).one()
            payload = conta_schema.dump(conta).data

        resp.body = json.dumps(payload, sort_keys=True)
        resp.status = falcon.HTTP_200
        session.close()

    #Cria uma conta
    @falcon.before(validate_conta_request)
    def on_post(self, req, resp):

        """
        :param objeto request HTTP:
        :param objeto response HTTP:
        :return: payload json

        recebe um json via request http
        """

        req_body = req.context['data']
        if req_body:
            session = Session()
            conta = Conta(req_body['tipo'], req_body['numero'], req_body['cliente_id'])
            if conta:

                session.add(conta)
                session.commit()
                session.close()
            else:
                raise ClienteNotExistsError("Cliente não existe")
        else:
            raise InvalidParameterError(req.context['data'])

        resp.status = falcon.HTTP_201
