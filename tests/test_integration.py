# pylint: disable=missing-docstring
from unittest.mock import patch
import pytest
from pymongo import MongoClient
from app import app

@pytest.fixture
def mongo_client():
    # Connect to mongoDB running locally in docker
    client = MongoClient("mongodb://localhost:27017/")
    # Yield the client to the test function
    yield client
    # Clean up the mongoDB after the test
    client.drop_database("test_database")

def test_post_route_inserts_to_mongodb(mongo_client):
    # Set up the test DB and collection
    db = mongo_client['test_database']
    collection = db['books']

    # Test book object

    #
