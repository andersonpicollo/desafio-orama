import falcon
from app.database import Session
from app.model import Conta
from app.model import Movimentacao
import json


class MovResource(object):

    # Credito
    def on_post(self, req, resp):

        """

        :param req: objeto request HTTP  {conta_id, valor}
        :param resp: objeto response HTTP
        :return:


        """

        request_body = json.loads(req.stream.read())
        session = Session()
        mov_request = Movimentacao('Credito', request_body['conta_id'], request_body['valor'])
        session.add(mov_request)
        conta = session.query(Conta).filter(Conta.id == mov_request.conta_id).one()
        conta.saldo += mov_request.valor
        session.commit()

        resp.status = falcon.HTTP_200

    # Debito
    def on_delete(self, req, resp):
        """

        :param req: objeto request HTTP  {conta_id, valor}
        :param resp: objeto response HTTP
        :return:


        """

        request_body = json.loads(req.stream.read())
        session = Session()
        mov_request = Movimentacao('Debito', request_body['conta_id'], request_body['valor'])
        session.add(mov_request)
        conta = session.query(Conta).filter(Conta.id == mov_request.conta_id).one()
        conta.saldo -= mov_request.valor
        session.commit()

        resp.status = falcon.HTTP_200

