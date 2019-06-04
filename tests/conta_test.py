from falcon import testing
import pytest
from app.resource import ContaResource
import falcon
from app.middleware import JsonParser


@pytest.fixture(scope="module")
def client():
    middleware = [JsonParser()]
    api = falcon.API(middleware=middleware)
    api.add_route('/contas', ContaResource())
    client = testing.TestClient(api)
    return client


def test_get_conta(client):
    resp = client.simulate_get('/contas')
    assert resp.status == falcon.HTTP_200






