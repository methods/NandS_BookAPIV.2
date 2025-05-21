
from app import app
import pytest
import uuid
import json

@pytest.fixture
def random_uuid():
    return str(uuid.uuid4())

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_helloworld_endpoint_returns_expected_results(client):
    response = client.get("/helloworld")

    assert response.status_code == 200
    assert "text" in response.content_type
    assert response.data.decode() == "hello world"

def test_add_book_creates_new_book(client, random_uuid):

    test_book = {
        "id": str(random_uuid),
        "title": "Test Book",
        "author": "AN Other",
        "synopsis": "Test Synopsis",
        "links": {
            "self": f'/books/{id}',
            "reservations": f'/books/{id}/reservations',
            "reviews": f'/books/{id}/reviews'
        }
    }

    response = client.post("/books", json = test_book)

    assert response.status_code == 201
    assert response.headers["content-type"] == "application/json"

    response_data = response.get_json()
    assert response_data == test_book