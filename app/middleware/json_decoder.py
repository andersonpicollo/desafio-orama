import json
import falcon

from app.exceptions import InvalidParameterError


class JsonParser(object):

    def process_request(self, req, res):
        if req.content_type == 'application/json':
            try:
                raw_json = req.stream.read()
            except Exception:
                message = "Não foi possivel ler o JSON"
                raise falcon.HTTPBadRequest(
                        "Requisição Invalida",
                        message
                )

            try:
                req.context['data'] = json.loads(raw_json.decode('utf-8'))
            except ValueError:
                raise InvalidParameterError('JSON object com formato invalido')
            except UnicodeError:
                raise InvalidParameterError('Não foi possivel ler o json')
        else:
            req.context['data'] = None

