"""Flask application module for managing a collection of books."""

from flask import Flask, request, jsonify
from data import books
import uuid
app = Flask(__name__)

@app.route("/books", methods=["POST"])
def add_book():
    """Flask application module for managing a collection of books."""
    # check if request is json
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    new_book = request.json
    if not isinstance(new_book, dict):
        return jsonify({"error": "JSON payload must be a dictionary"}), 400

    # create UUID and add it to the new_book object
    new_book_id = str(uuid.uuid4())
    new_book["id"] = new_book_id

    # validation
    required_fields = ["title", "synopsis", "author"]
    for field in required_fields:
        if field not in new_book:
            return {"error": f"Missing required fields: {field}"}, 400


    new_book['links'] = {
        'self': f'/books/{new_book_id}',
        'reservations': f'/books/{new_book_id}/reservations',
        'reviews': f'/books/{new_book_id}/reviews'
    }

    # Map field names to their expected types
    field_types = {
        "id": str,
        "title": str,
        "synopsis": str,
        "author": str,
        "links": dict
    }

    for field, expected_type in field_types.items():
        if not isinstance(new_book[field], expected_type):
            return {"error": f"Field {field} is not of type {expected_type}"}, 400

    # Check the types of nested fields in links
    links_field_types = {
        "self": str,
        "reservations": str,
        "reviews": str
    }

    for nested_field, nested_expected_type in links_field_types.items():
        if not isinstance(new_book['links'][nested_field], nested_expected_type):
            return {
                "error": f"Field 'links.{nested_field}' is not of type {nested_expected_type}"
                }, 400

    books.append(new_book)

    return jsonify(books[-1]), 201
