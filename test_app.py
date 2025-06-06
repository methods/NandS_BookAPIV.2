# pylint: disable=missing-docstring
from unittest.mock import patch
import pytest
from app import app

# Option 1: Rename the fixture to something unique (which I've used)
# Option 2: Use a linter plugin that understands pytest
@pytest.fixture(name="client")
def client_fixture():
    app.config['TESTING'] = True
    return app.test_client()

# ------------------- Tests for POST ---------------------------------------------

def test_add_book_creates_new_book(client):

    test_book = {
        "title": "Test Book",
        "author": "AN Other",
        "synopsis": "Test Synopsis"
    }

    response = client.post("/books", json = test_book)

    assert response.status_code == 201
    assert response.headers["content-type"] == "application/json"

    response_data = response.get_json()
    required_fields = ["id", "title", "synopsis", "author", "links"]
    # check that required fields are in the response data
    for field in required_fields:
        assert field in response_data, f"{field} not in response_data"

def test_add_book_sent_with_missing_required_fields(client):
    test_book = {
        "author": "AN Other"
        # missing 'title' and 'synopsis'
    }
    response = client.post("/books", json = test_book)

    assert response.status_code == 400
    response_data = response.get_json()
    assert 'error' in response_data
    assert "Missing required fields: title, synopsis" in response.get_json()["error"]


def test_add_book_sent_with_wrong_types(client):
    test_book = {
        "title": 1234567,
        "author": "AN Other",
        "synopsis": "Test Synopsis"
    }

    response = client.post("/books", json = test_book)

    assert response.status_code == 400
    response_data = response.get_json()
    assert 'error' in response_data
    assert "Field title is not of type <class 'str'>" in response.get_json()["error"]

def test_add_book_with_invalid_json_content(client):

    # This should trigger a TypeError
    response = client.post("/books", json ="This is not a JSON object")

    assert response.status_code == 400
    assert "JSON payload must be a dictionary" in response.get_json()["error"]

def test_add_book_check_request_header_is_json(client):

    response = client.post(
        "/books",
        data ="This is not a JSON object",
        headers = {"content-type": "text/plain"}
    )

    assert response.status_code == 415
    assert "Request must be JSON" in response.get_json()["error"]

def test_500_response_is_json(client):
    test_book = {
        "title": "Valid Title",
        "author": "AN Other",
        "synopsis": "Test Synopsis"
    }

    # Use patch to mock uuid module failing and throwing an exception
    with patch("uuid.uuid4", side_effect=Exception("An unexpected error occurred")):
        response = client.post("/books", json = test_book)

        # Check the response code is 500
        assert response.status_code == 500

        assert response.content_type == "application/json"
        assert "An unexpected error occurred" in response.get_json()["error"]

# ------------------------ Tests for GET --------------------------------------------
def test_get_all_books_returns_all_books(client):
    response = client.get("/books")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    response_data = response.get_json()
    assert isinstance(response_data, dict)
    assert 'total_count' in response_data
    assert 'items' in response_data

def test_return_error_404_when_list_is_empty(client):
    with patch("app.books", []):
        response = client.get("/books")
        assert response.status_code == 404
        assert "No books found" in response.get_json()["error"]

def test_get_books_returns_404_when_books_is_none(client):
    with patch("app.books", None):
        response = client.get("/books")
        assert response.status_code == 404
        assert "No books found" in response.get_json()["error"]

def test_missing_fields_in_book_object_returned_by_database(client):
    with patch("app.books", [
        {
            "id": "1",
            "title": "The Great Adventure",
            "synopsis": "A thrilling adventure through the jungles of South America.",
            "author": "Jane Doe"
        },
        {
            "id": "2",
            "title": "Mystery of the Old Manor"
        },
        {
            "id": "3",
            "title": "The Science of Everything",
            "synopsis": "An in-depth look at the scientific principles that govern our world."
        }
    ]):
        response = client.get("/books")
        assert response.status_code == 500
        assert "Missing fields" in response.get_json()["error"]


 #-------- Tests for filter GET /books by delete ----------------
def test_get_books_excludes_deleted_books_and_omits_state_field(client):
    # Add a book so we have a known ID
    with patch("app.books", [
        {
            "id": "1",
            "title": "The Great Adventure",
            "synopsis": "A thrilling adventure through the jungles of South America.",
            "author": "Jane Doe",
            "links": {
                "self": "/books/1",
                "reservations": "/books/1/reservations",
                "reviews": "/books/1/reviews"
            },
            "state": "deleted"
        },
        {
            "id": "2",
            "title": "Mystery of the Old Manor",
            "synopsis": "A detective story set in an old manor with many secrets.",
            "author": "John Smith",
            "links": {
                "self": "/books/2",
                "reservations": "/books/2/reservations",
                "reviews": "/books/2/reviews"
            },
            "state": "active"
        },
        {
            "id": "3",
            "title": "The Science of Everything",
            "synopsis": "An in-depth look at the scientific principles that govern our world.",
            "author": "Alice Johnson",
            "links": {
                "self": "/books/3",
                "reservations": "/books/3/reservations",
                "reviews": "/books/3/reviews"
            }
        }
    ]):
        response = client.get("/books")
        assert response.status_code == 200

        data = response.get_json()
        assert "items" in data
        books = data["items"]

        # Check right object is returned
        assert len(books) == 2
        for book in books:
            assert "state" not in book
        assert books[0].get("id") == '2'
        assert books[1].get("title") == "The Science of Everything"

 #-------- Tests for GET a single resource ----------------

def test_get_book_returns_specified_book(client):
    # Add a book so we have a known ID
    new_book = {
        "title": "1984",
        "synopsis": "Dystopian novel about surveillance and control.",
        "author": "George Orwell"
    }

    post_response = client.post("/books", json=new_book)
    assert post_response.status_code == 201

    # Extract the ID from the response
    book_data = post_response.get_json()
    book_id = book_data["id"]


    # Test GET request using the book ID
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 200
    assert get_response.content_type == "application/json"
    returned_book = get_response.get_json()
    assert returned_book["id"] == book_id
    assert returned_book["title"] == "1984"

def test_get_book_not_found_returns_404(client):
    # Test GET request using invalid book ID
    response = client.get("/books/12341234")
    assert response.status_code == 404
    assert response.content_type == "application/json"
    assert "Book not found" in response.get_json()["error"]

def test_invalid_urls_return_404(client):
    # Test invalid URL
    response = client.get("/books/")
    assert response.status_code == 404
    assert response.content_type == "application/json"
    assert "404 Not Found" in response.get_json()["error"]

def test_book_database_is_initialized_for_specific_book_route(client):
    with patch("app.books", None):
        response = client.get("/books/1")
        assert response.status_code == 500
        assert "Book collection not initialized" in response.get_json()["error"]


def test_get_book_returns_404_if_state_equals_deleted(client):
    book_id = "3"
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404
    assert response.content_type == "application/json"
    assert "Book not found" in response.get_json()["error"]

# ------------------------ Tests for DELETE --------------------------------------------
# Mock book database object

books_database = [
        {
            "id": "1",
            "title": "The Great Adventure",
            "synopsis": "A thrilling adventure through the jungles of South America.",
            "author": "Jane Doe",
            "links": {
                "self": "/books/1",
                "reservations": "/books/1/reservations",
                "reviews": "/books/1/reviews"
            },
            "state": "active"
        },
        {
            "id": "2",
            "title": "Mystery of the Old Manor",
            "synopsis": "A detective story set in an old manor with many secrets.",
            "author": "John Smith",
            "links": {
                "self": "/books/2",
                "reservations": "/books/2/reservations",
                "reviews": "/books/2/reviews"
            },
            "state": "active"
        },
        {
            "id": "3",
            "title": "The Science of Everything",
            "synopsis": "An in-depth look at the scientific principles that govern our world.",
            "author": "Alice Johnson",
            "links": {
                "self": "/books/3",
                "reservations": "/books/3/reservations",
                "reviews": "/books/3/reviews"
            },
            "state": "deleted"
        }
    ]

def test_book_is_soft_deleted_on_delete_request(client):
    with patch("app.books", books_database):
        # Send DELETE request
        book_id = '1'
        response = client.delete(f"/books/{book_id}")

        assert response.status_code == 204
        assert response.data == b''
        # check that the book's state has changed to deleted
        assert books_database[0]['state'] == 'deleted'


def test_delete_empty_book_id(client):
    book_id =""
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 404
    assert response.content_type == "application/json"
    assert "404 Not Found" in response.get_json()["error"]

def test_delete_invalid_book_id(client):
    response = client.delete("/books/12341234")
    assert response.status_code == 404
    assert response.content_type == "application/json"
    assert "Book not found" in response.get_json()["error"]

def test_book_database_is_initialized_for_delete_book_route(client):
    with patch("app.books", None):
        response = client.delete("/books/1")
        assert response.status_code == 500
        assert "Book collection not initialized" in response.get_json()["error"]
