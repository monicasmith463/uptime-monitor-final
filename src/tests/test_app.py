import pytest

from src.app import app as main_app


@pytest.fixture()
def app():

    
    main_app.config["TESTING"] = True
    yield main_app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_main(client):
    response = client.get("/")
    assert response.status_code == 200


def skip_test_add_site(client):
    form_data = {"site": "https://example153.com"} 

    response = client.post("/", data=form_data)
    assert response.status_code == 200 or response.status_code == 302


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200