import pytest
from src.app import main

@pytest.fixture()
def app():
    app = main()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()

def test_main():
    pass

def test_add_site():
    pass