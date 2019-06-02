import falcon
from cerberus import Validator
from cerberus.errors import ValidationError
from app.database import Session,engine
from app.model import Conta
from app.schemas import ContaSchema, MovSchema
from app.model import Movimentacao
from app.exceptions import InvalidParameterError
from app.exceptions import InvalidMovError
from app.exceptions import InvalidDateError
from datetime import datetime
from sqlalchemy.sql import text
import json

FIELDS = {

        'conta_id': {
            'type': 'integer',
            'required': True
        },
        'valor': {
            'type': 'float',
            'required': True,
        }
}


def validate_mov_request(req, res, resource, params):
    schema = {
        'conta_id': FIELDS['conta_id'],
        'valor':    FIELDS['valor']
    }

    validator = Validator(schema)

    try:
        if not validator.validate(req.context['data']):
            raise InvalidParameterError(validator.errors)
    except ValidationError:
        raise InvalidParameterError('Invalid Request %s' % req.context)


class MovResource(object):

    def on_get(self, req, resp, conta_id=None, date_inicio=None, date_fim=None):

        if not conta_id:
            raise InvalidParameterError("Conta inexistente")

        try:
            date_inicio = datetime.strptime(date_inicio, "%Y-%m-%d") or datetime.today().strftime('%Y-%m-%d')
            date_fim = datetime.strptime(date_fim, "%Y-%m-%d") or datetime.today().strftime('%Y-%m-%d')
        except ValueError:
            raise InvalidDateError("Alguma data invalida")

        if not date_fim < date_inicio:
            session = Session()
            mov_schema = MovSchema()

            movs = session.query(Movimentacao).filter(Movimentacao.conta_id == conta_id,\
                                                      Movimentacao.created >= date_inicio,\
                                                      Movimentacao.created <= date_fim).all()
            payload = []
            for mov in movs:
                mov_to_schema = mov_schema.dump(mov).data
                payload.append(mov_to_schema)

            movs = json.dumps(payload, sort_keys=True)
            resp.body = json.dumps(payload, sort_keys=True)
            resp.status = falcon.HTTP_200
            session.close

        else:
            raise InvalidDateError("Data fim maior que data inicio")


    # Credit
    @falcon.before(validate_mov_request)
    def on_post(self, req, resp):

        """
        :param req: objeto request HTTP  {conta_id, valor}
        :param resp: objeto response HTTP
        :return:
        """

        req_body = req.context['data']
        if req_body:

            if req_body['valor'] <= 0:
                raise InvalidMovError("Valor inferior a zero")

            session = Session()
            conta = session.query(Conta).filter(Conta.id == req_body['conta_id']).first()
            if not conta:
                raise InvalidMovError("Conta não existe")

            try:
                mov = Movimentacao('credito', req_body['conta_id'], req_body['valor'])
                session.add(mov)
                conta.saldo += req_body['valor']
                session.commit()
            except Exception:
                session.rollback()
        else:
            raise InvalidMovError(req.context['data'])

        resp.status = falcon.HTTP_200

    # Debit
    def on_delete(self, req, resp):
        """

        :param req: objeto request HTTP  {conta_id, valor}
        :param resp: objeto response HTTP
        :return:
        """
        req_body = req.context['data']
        if req_body:

            if req_body['valor'] <= 0:
                raise InvalidMovError("Valor inferior a zero")

            session = Session()
            conta = session.query(Conta).filter(Conta.id == req_body['conta_id']).first()
            if not conta:
                raise InvalidMovError("Conta não existe")

            try:
                mov = Movimentacao('debito', req_body['conta_id'], req_body['valor'])
                session.add(mov)
                conta.saldo -= req_body['valor']
                session.commit()
            except Exception:
                session.rollback()
        else:
            raise InvalidMovError(req.context['data'])

        resp.status = falcon.HTTP_200

