from tests.test_main import client

def test_healthcheck():
    response = client.get("/api/v1/healthcheck")
    assert response.status_code == 200
