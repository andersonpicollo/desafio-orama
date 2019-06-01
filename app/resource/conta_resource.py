import falcon
import json
from app.database import Session
from app.schemas import ContaSchema
from app.model import Conta
from app.model import Movimentacao


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
    def on_post(self, req, resp):

        """
        :param objeto request HTTP:
        :param objeto response HTTP:
        :return: payload json

        recebe um json via request http
        """

        session = Session
        conta_schema = ContaSchema()
        request_body = json.loads(req.stream.read())
        conta = Conta(request_body['tipo'], request_body['numero'], request_body['cliente_id'])
        session.add(conta)
        session.commit()
        session.close()
        resp.status = falcon.HTTP_201
