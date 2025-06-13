# pylint: disable=missing-docstring
import json
import pytest
from pymongo import MongoClient
from app import app


@pytest.fixture(name="client")
def client_fixture():
    """Provides a test client for making requests to our Flask app."""
    app.config['TESTING'] = True
    return app.test_client()


@pytest.fixture
def mongo_client():
    # Connect to mongoDB running locally in docker
    client = MongoClient("mongodb://localhost:27017/")
    # Yield the client to the test function
    yield client
    # Clean up the mongoDB after the test
    client.drop_database("test_database")

def test_post_route_inserts_to_mongodb(mongo_client, client):
    # Set up the test DB and collection
    db = mongo_client['test_database']
    collection = db['books']

    # Arrange: Test book object
    new_book_payload = {
        "title": "The Midnight Library",
        "synopsis": "A novel about all the choices that go into a life well lived.",
        "author": "Matt Haig"
    }

    # Act- send the POST request:
    response = client.post(
        "/books", 
        # json.dumps() serializes dict into a JSON formatted string
        data=json.dumps(new_book_payload),
        content_type="application/json"
    )

    # Assert:
    assert response.status_code == 201
    assert response.headers["content-type"] == "application/json"

    # Assert database state directly:
    saved_book = collection.find_one({"title": "The Midnight Library"})
    assert saved_book is not None
    assert saved_book["author"] == "Matt Haig"
