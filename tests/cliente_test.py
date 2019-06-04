from falcon import testing
import pytest
from app.resource import ClienteResource
import falcon
from app.middleware import JsonParser


@pytest.fixture(scope="module")
def client():
    middleware = [JsonParser()]
    api = falcon.API(middleware=middleware)
    api.add_route('/clientes', ClienteResource())
    client = testing.TestClient(api)
    return client


def test_get_conta(client):
    resp = client.simulate_get('/clientes')
    assert resp.status == falcon.HTTP_200






