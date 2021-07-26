from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code != 500
    assert response.json() == {
        "message": "Burger delivery service. You're welcome"}


def test_read_all():
    response = client.get("/burgers/")
    assert response.status_code != 500


def test_read_single():
    response = client.get("/burger/4")
    assert response.status_code != 500


print("All tests run as expected")
